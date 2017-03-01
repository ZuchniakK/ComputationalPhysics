import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def calculate_weights(G, initial_nodes, pos, edge_dict, show=False):
    nodes_distance = {}
    nodes_weight = {}
    nodes_distance[initial_nodes] = 0
    nodes_weight[initial_nodes] = 1
    actual_neighbors = []
    done_nodes = [initial_nodes]

    for i in G.neighbors(initial_nodes):
        nodes_distance[i] = 1
        nodes_weight[i] = 1
        actual_neighbors.append(i)

    while len(actual_neighbors) > 0:
        new_neighbors = []
        for actual_neighbor in actual_neighbors:
            for j in G.neighbors(actual_neighbor):
                if j not in nodes_distance:
                    nodes_distance[j] = nodes_distance[actual_neighbor] + 1
                    nodes_weight[j] = nodes_weight[actual_neighbor]
                elif nodes_distance[j] == nodes_distance[actual_neighbor] + 1:
                    nodes_weight[j] += nodes_weight[actual_neighbor]
                new_neighbors.append(j)
            done_nodes.append(actual_neighbor)
        new_neighbors = list(set(new_neighbors))
        new_neighbors = list(filter(lambda el: el not in done_nodes, new_neighbors))
        actual_neighbors = new_neighbors.copy()
        new_neighbors.clear()

    # finding leaf
    max_distance = max(nodes_distance.values())
    keys_of_max_distance = [key for key, value in nodes_distance.items() if value == max_distance]

    done_nodes.clear()
    # iterating over leaf
    for leaf in keys_of_max_distance:
        for leaf_neighbor in G.neighbors(leaf):
            if (leaf, leaf_neighbor) in edge_dict:
                if nodes_distance[leaf] > nodes_distance[leaf_neighbor]:
                    edge_dict[(leaf, leaf_neighbor)] = nodes_weight[leaf_neighbor] / nodes_weight[leaf]
                else:
                    edge_dict[(leaf, leaf_neighbor)] = 0
            else:
                if nodes_distance[leaf] > nodes_distance[leaf_neighbor]:
                    edge_dict[(leaf_neighbor, leaf)] = nodes_weight[leaf_neighbor] / nodes_weight[leaf]
                else:
                    edge_dict[(leaf_neighbor, leaf)] = 0
        done_nodes.append(leaf)

    for distance_level in range(max_distance - 2, -1, -1):
        keys_of_actual_distance = [key for key, value in nodes_distance.items() if value == distance_level]
        for up_node in keys_of_actual_distance:
            up_node_neighbours = G.neighbors(up_node)
            up_node_down_neighbours = list(
                filter(lambda el: nodes_distance[el] > nodes_distance[up_node], up_node_neighbours))
            for down_node in up_node_down_neighbours:
                tmp_weight = 1
                down_node_neighbors = G.neighbors(down_node)
                down_down_nodes = list(
                    filter(lambda el: nodes_distance[el] > nodes_distance[down_node], down_node_neighbors))
                for down_down_node in down_down_nodes:
                    if (down_node, down_down_node) in edge_dict:
                        tmp_weight += edge_dict[(down_node, down_down_node)]
                    else:
                        tmp_weight += edge_dict[(down_down_node, down_node)]
                tmp_weight *= nodes_weight[up_node] / nodes_weight[down_node]
                if (up_node, down_node) in edge_dict:
                    edge_dict[(up_node, down_node)] = tmp_weight
                else:
                    edge_dict[(down_node, up_node)] = tmp_weight
    if show:
        edge_dict_round = {}
        for key in edge_dict:
            edge_dict_round[key] = round(edge_dict[key], 2)
        nx.draw_networkx_nodes(G, pos, alpha=0.4, node_color=list(nodes_distance.values()))
        nx.draw_networkx_edges(G, pos, edge_color=list(edge_dict.values()))
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_dict_round, label_pos=0.4)
        nx.draw_networkx_labels(G, pos, labels=nodes_weight)
        plt.show()
    return edge_dict, nodes_distance, nodes_weight


def calculate_intensity_of_edges(G, pos, edge_dict, show=True):
    total_edges_weight = {}
    for key in edge_dict:
        total_edges_weight[key] = 0
    for key in pos:
        edge_weight_dict, distance_dict, node_weight_dict = calculate_weights(G, key, pos, edge_dict)
        for key2 in edge_weight_dict:
            total_edges_weight[key2] += edge_weight_dict[key2]
    edge_dict_round = {}
    for key in total_edges_weight:
        edge_dict_round[key] = round(total_edges_weight[key], 2)
    nx.draw_networkx_nodes(G, pos, alpha=0.4, node_color='r')
    nx.draw_networkx_edges(G, pos, edge_color=list(edge_dict.values()))
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_dict_round, label_pos=0.4)
    nx.draw_networkx_labels(G, pos)
    plt.title("Edge weights")
    plt.show()
    strong_edge = max(total_edges_weight, key=total_edges_weight.get)
    G.remove_edge(*strong_edge)
    del total_edges_weight[strong_edge]
    del edge_dict[strong_edge]
    return strong_edge


def find_community_1(G, pos, edge_dict, show=False):
    is_connected = nx.is_connected(G)
    while is_connected:
        is_connected = nx.is_connected(G)
        calculate_intensity_of_edges(G, pos, edge_dict, show=show)


def random_walk_intensity_of_edges(G, pos, edge_dict, show=False, repeat=1):
    node_list = nx.nodes(G)
    print(node_list)
    for repeat_time in range(repeat):
        for i_node in node_list:
            for j_node in node_list:
                if nx.has_path(G, i_node, j_node):
                    actual_node = i_node

                    while actual_node != j_node:
                        while True:
                            next_neighbour = np.random.choice(G.neighbors(actual_node))
                            if nx.shortest_path_length(G, next_neighbour, j_node) < nx.shortest_path_length(G,
                                                                                                            actual_node,
                                                                                                            j_node):
                                break

                        if (actual_node, next_neighbour) in edge_dict:
                            edge_dict[actual_node, next_neighbour] += 1 / repeat
                        else:
                            edge_dict[next_neighbour, actual_node] += 1 / repeat
                        actual_node = next_neighbour

    edge_dict_round = {}
    for key in edge_dict:
        edge_dict_round[key] = round(edge_dict[key], 2)
    nx.draw_networkx_nodes(G, pos, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=[i_node, j_node], node_color='g')
    nx.draw_networkx_nodes(G, pos, nodelist=[actual_node], node_color='y')
    nx.draw_networkx_edges(G, pos, edge_color=list(edge_dict.values()))
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_dict_round, label_pos=0.4)
    plt.title("Edge weights")
    plt.show()
    strong_edge = max(edge_dict, key=edge_dict.get)
    G.remove_edge(*strong_edge)
    del edge_dict[strong_edge]
    return strong_edge


def find_community_2(G, pos, edge_dict, show=False, repeat=1):
    is_connected = nx.is_connected(G)
    while is_connected:
        is_connected = nx.is_connected(G)
        random_walk_intensity_of_edges(G, pos, edge_dict, show=True, repeat=1)


if __name__ == '__main__':
    pos = {
        1: [1, 4],
        2: [2, 5],
        3: [3, 5],
        4: [4, 4],
        5: [3, 3],
        6: [2, 3],
        7: [4, 1],
        8: [4.5, 2],
        9: [5.5, 2],
        10: [5, 1],
        11: [6, 1],
    }
    edge_dict = {
        (1, 2): 0,
        (1, 3): 0,
        (1, 4): 0,
        (1, 5): 0,
        (1, 6): 0,
        (2, 3): 0,
        (2, 4): 0,
        (2, 5): 0,
        (2, 6): 0,
        (3, 4): 0,
        (3, 5): 0,
        (3, 6): 0,
        (4, 5): 0,
        (4, 6): 0,
        (5, 6): 0,

        (4, 8): 0,
        (5, 7): 0,

        (7, 8): 0,
        (7, 9): 0,
        (7, 10): 0,
        (8, 9): 0,
        (8, 10): 0,
        (8, 11): 0,
        (9, 10): 0,
        (9, 11): 0,
        (10, 11): 0,

    }
    pos2 = {
        1: [1, 1],
        2: [1, 2],
        3: [2, 2],
        4: [2, 1],
        5: [3, 1],
        6: [3, 2],
        7: [4, 1]
    }
    edge_dict2 = {
        (1, 2): 0,
        (1, 3): 0,
        (1, 4): 0,
        (2, 3): 0,
        (2, 4): 0,
        (3, 4): 0,
        (3, 6): 0,
        (4, 5): 0,
        (5, 6): 0,
        (5, 7): 0,
        (6, 7): 0

    }

    G = nx.Graph()
    G.add_nodes_from(pos.keys())
    G.add_edges_from(edge_dict.keys())
    find_community_1(G, pos, edge_dict, show=True)
    G2 = nx.Graph()
    G2.add_nodes_from(pos2.keys())
    G2.add_edges_from(edge_dict2.keys())
    find_community_2(G2, pos2, edge_dict2, show=True)
