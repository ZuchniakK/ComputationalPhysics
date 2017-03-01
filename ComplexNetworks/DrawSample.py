import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_random_geometric_graph(n, radius):
    # Generate random graph
    G = nx.random_geometric_graph(n, radius)
    pos = nx.get_node_attributes(G, 'pos')  # Get positions of nodes
    nx.draw(G)
    plt.show()

    # find node nearest the center point (0.5,0.5)
    dists = [(x - 0.5) ** 2 + (y - 0.5) ** 2 for x, y in list(pos.values())]
    ncenter = np.argmin(dists)
    # Plot graph, coloring by path length from central node
    p = nx.single_source_shortest_path_length(G, ncenter)
    k = G.degree()
    print(p)
    plt.figure()
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                           node_size=120, alpha=0.5,
                           node_color=list(k.values()), cmap=plt.cm.jet_r)
    plt.title('n=%s, radius=%s' % (n, radius))
    plt.show()


if __name__ == '__main__':
    plot_random_geometric_graph(60, 0.4)
