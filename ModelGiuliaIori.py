import numpy
from math import pow, log
from matplotlib.pylab import *


def model(L, variance, A, prawd, consultation_type="give_info", analize=0):
    # model parameters
    p_0 = 1
    mean = 0
    B = 0
    J = numpy.ones((L, L)) * prawd
    T = 200

    # create vectors
    time = []
    r = []
    price_in_time = []

    signal = numpy.zeros((L, L))
    if variance != 0:
        threshold_up = abs(numpy.random.normal(mean, variance, (L, L)))
    else:
        threshold_up = numpy.ones((L, L)) * mean
    threshold_down = numpy.zeros((L, L))
    for i in range(L):
        for j in range(L):
            threshold_down[i, j] = mean - threshold_up[i, j]
    price = p_0

    for t in range(T):
        d_vector = []
        z_vector = []
        consulting_vector = []
        random__matrix = numpy.zeros((L, L))
        aggregate_signal = B * numpy.random.uniform(-1, 1)

        for i in range(L):
            for j in range(L):
                random__matrix[i, j] = A * numpy.random.uniform(-1, 1) + aggregate_signal
        signal = numpy.zeros((L, L))

        for i in range(L):
            for j in range(L):
                if random__matrix[i, j] >= threshold_up[i, j]:
                    signal[i, j] = 1
                elif random__matrix[i, j] <= threshold_down[i, j]:
                    signal[i, j] = -1
                else:
                    signal[i, j] = 0

        if analize == 1:
            matshow(signal)
            plt.colorbar()
            show()

        left = numpy.zeros((L, L))
        right = numpy.zeros((L, L))
        up = numpy.zeros((L, L))
        down = numpy.zeros((L, L))

        for i in range(L):
            for j in range(L):
                left[i, j] = int(numpy.random.uniform(0, 1) < J[i, j])
                right[i, j] = int(numpy.random.uniform(0, 1) < J[i, j])
                up[i, j] = int(numpy.random.uniform(0, 1) < J[i, j])
                down[i, j] = int(numpy.random.uniform(0, 1) < J[i, j])

        for consulting in range(120):
            Y = numpy.zeros((L, L))
            for i in range(L):
                for j in range(L):
                    Y[i, j] = random__matrix[i, j]
            if consultation_type == "give_info":
                for i in range(L):
                    for j in range(L):
                        i_up = i - 1
                        i_down = i + 1
                        j_right = j + 1
                        j_left = j - 1
                        if i_up == -1:
                            i_up = L - 1
                        if i_down == L:
                            i_down = 0
                        if j_right == L:
                            j_right = 0
                        if j_left == -1:
                            j_left = L - 1

                        Y[i_up, j] += up[i, j] * signal[i, j]
                        Y[i_down, j] += down[i, j] * signal[i, j]
                        Y[i, j_right] += right[i, j] * signal[i, j]
                        Y[i, j_left] += left[i, j] * signal[i, j]

                for i in range(L):
                    for j in range(L):
                        if Y[i, j] >= threshold_up[i, j]:

                            signal[i, j] = 1
                        elif Y[i, j] <= threshold_down[i, j]:

                            signal[i, j] = -1
                        else:
                            signal[i, j] = 0
                if analize == 1:
                    d = (signal == 1).sum()
                    z = (signal == -1).sum()
                    d_vector.append(d / L ** 2)
                    z_vector.append(z / L ** 2)
                    consulting_vector.append(consulting)
            if consultation_type == "get_info":
                for i in range(L):
                    for j in range(L):
                        i_up = i - 1
                        i_down = i + 1
                        j_right = j + 1
                        j_left = j - 1
                        if i_up == -1:
                            i_up = L - 1
                        if i_down == L:
                            i_down = 0
                        if j_right == L:
                            j_right = 0
                        if j_left == -1:
                            j_left = L - 1

                        Y[i, j] += up[i_up, j] * signal[i_up, j] \
                                   + down[i_down, j] * signal[i_down, j] \
                                   + right[i, j_right] * signal[i, j_right] \
                                   + left[i, j_left] * signal[i, j_left]

                        if Y[i, j] >= threshold_up[i, j]:
                            signal[i, j] = 1
                        elif Y[i, j] <= threshold_down[i, j]:
                            signal[i, j] = -1
                        else:
                            signal[i, j] = 0

                if analize == 1:
                    d = (signal == 1).sum()
                    z = (signal == -1).sum()
                    d_vector.append(d / L ** 2)
                    z_vector.append(z / L ** 2)
                    consulting_vector.append(consulting)

            if consultation_type == "random_walk":
                i = numpy.random.randint(0, L)
                j = numpy.random.randint(0, L)
                for p in range(L ** 2):
                    i += numpy.random.randint(0, 2) * 2 - 1
                    j += numpy.random.randint(0, 2) * 2 - 1
                    if i == -1:
                        i = L - 1
                    if i == L:
                        i = 0
                    if j == L:
                        j = 0
                    if j == -1:
                        j = L - 1

                    i_up = i - 1
                    i_down = i + 1
                    j_right = j + 1
                    j_left = j - 1
                    if i_up == -1:
                        i_up = L - 1
                    if i_down == L:
                        i_down = 0
                    if j_right == L:
                        j_right = 0
                    if j_left == -1:
                        j_left = L - 1

                    Y[i, j] += up[i_up, j] * signal[i_up, j] \
                               + down[i_down, j] * signal[i_down, j] \
                               + right[i, j_right] * signal[i, j_right] \
                               + left[i, j_left] * signal[i, j_left]

                    if Y[i, j] >= threshold_up[i, j]:
                        signal[i, j] = 1
                    elif Y[i, j] <= threshold_down[i, j]:
                        signal[i, j] = -1
                    else:
                        signal[i, j] = 0

                if analize == 1:
                    d = (signal == 1).sum()
                    z = (signal == -1).sum()
                    d_vector.append(d / L ** 2)
                    z_vector.append(z / L ** 2)
                    consulting_vector.append(consulting)

        if analize == 1:
            plt.plot(consulting_vector, d_vector, consulting_vector, z_vector)
            show()
            matshow(signal)
            plt.colorbar()
            show()

        d = (signal == 1).sum()
        z = (signal == -1).sum()

        if d < 1:
            d = 1
        if z < 1:
            z = 1
        alfa = (z + d) / pow(L, 2)
        income = pow(d / z, alfa)
        price_new = price * income
        threshold_up *= income
        threshold_down *= income

        time.append(t)
        r.append(log(price_new / price))
        price_in_time.append(price)
        price = price_new
    plt.title('Market activity distribution')
    subplot(2, 2, 1)
    plt.hist(r, 50, normed=True)
    plt.title('Market activity distribution')

    subplot(2, 1, 2)
    plt.plot(time, r)
    plt.title('Interest rate')

    subplot(2, 2, 2)
    plt.plot(time, price_in_time)
    plt.title('Price in time')

    plt.show()
    matshow(signal)
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    model(10, 0, 0.2, 0.4)
