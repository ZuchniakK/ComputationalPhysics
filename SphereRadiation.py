import matplotlib.pyplot as plt
from numpy.random import random  as rand
from numpy import pi as  PI
from numpy import cos as cos
from numpy import sin as sin
from numpy import linspace as linspace
from numpy import var
import time


def cos_distribution(n):
    rand_vector = []
    iterator = 0
    while iterator < n:
        x = PI * rand() - PI / 2
        y = rand()
        if y <= cos(x):
            rand_vector.append(x)
            iterator += 1
    return rand_vector


def vector_generator(n):
    theta = cos_distribution(n)
    phi = [rand() * PI * 2 for i in range(n)]
    X = [cos(i) * cos(j) for i, j in zip(theta, phi)]
    Y = [cos(i) * sin(j) for i, j in zip(theta, phi)]
    Z = [sin(i) for i in theta]
    return X, Y, Z


def add_light(x, y, z, bins=20, pXstart=0.5, pYstart=0.5, pZstart=0.5, Xmax=1, Ymax=1, Zmax=1, reflex_factor=0.8,
              min_intense=0.2):
    down = 0
    up = 0
    front = 0
    back = 0
    left = 0
    right = 0

    xground = []
    yground = []
    xp = []
    yp = []
    sample_lenght = len(x)
    power = [1 for i in range(sample_lenght)]
    vXstart = [pXstart for i in range(sample_lenght)]
    vYstart = [pYstart for i in range(sample_lenght)]
    vZstart = [pZstart for i in range(sample_lenght)]
    final_power = []
    for (i, j, k, po, Xstart, Ystart, Zstart) in zip(x, y, z, power, vXstart, vYstart, vZstart):

        zydeltaL = -Ystart
        zydeltaR = Ymax - Ystart
        zxdeltaL = -Xstart
        zxdeltaR = Xmax - Xstart

        yxdeltaL = -Xstart
        yxdeltaR = Xmax - Xstart
        yzdeltaL = -Zstart
        yzdeltaR = Zmax - Zstart

        xydeltaL = -Ystart
        xydeltaR = Ymax - Ystart
        xzdeltaL = -Zstart
        xzdeltaR = Zmax - Zstart

        h1 = Zstart
        if k < 0 and j / abs(k) > zydeltaL / h1 and j / abs(k) < zydeltaR / h1 and i / abs(
                k) > zxdeltaL / h1 and i / abs(k) < zxdeltaR / h1:
            down += 1
            xground.append(Xstart + i / abs(k) * h1)
            yground.append(Ystart + j / abs(k) * h1)
            final_power.append(po)

        h2 = Zmax - Zstart
        if k > 0 and j / k > zydeltaL / h2 and j / k < zydeltaR / h2 and i / k > zxdeltaL / h2 and i / k < zxdeltaR / h2:
            up += 1
            if po > min_intense:
                vXstart.append(Xstart + i / k * h2)
                vYstart.append(Ystart + j / k * h2)
                vZstart.append(Zmax)
                power.append(po * reflex_factor)
                x.append(i)
                y.append(j)
                z.append(-k)

        h3 = Ystart
        if j < 0 and i / abs(j) > yxdeltaL / h3 and i / abs(j) < yxdeltaR / h3 and k / abs(
                j) > yzdeltaL / h3 and k / abs(j) < yzdeltaR / h3:
            front += 1
            if po > min_intense:
                vXstart.append(Xstart - i / j * h3)
                vZstart.append(Zstart - k / j * h3)
                vYstart.append(0)
                power.append(po * reflex_factor)
                x.append(i)
                y.append(-j)
                z.append(k)
        h4 = Ymax - Ystart
        if j > 0 and i / j > yxdeltaL / h4 and i / j < yxdeltaR / h4 and k / j > yzdeltaL / h4 and k / j < yzdeltaR / h4:
            back += 1
            if po > min_intense:
                vXstart.append(Xstart + i / j * h4)
                vZstart.append(Zstart + k / j * h4)
                vYstart.append(Ymax)
                power.append(po * reflex_factor)
                x.append(i)
                y.append(-j)
                z.append(k)
        h5 = Xstart
        if i < 0 and j / abs(i) > xydeltaL / h5 and j / abs(i) < xydeltaR / h5 and k / abs(
                i) > xzdeltaL / h5 and k / abs(i) < xzdeltaR / h5:
            left += 1
            if po > min_intense:
                vYstart.append(Ystart - j / i * h5)
                vZstart.append(Zstart - k / i * h5)
                vXstart.append(0)
                power.append(po * reflex_factor)
                x.append(-i)
                y.append(j)
                z.append(k)

        h6 = Xmax - Xstart
        if i > 0 and j / i > xydeltaL / h6 and j / i < xydeltaR / h6 and k / i > xzdeltaL / h6 and k / i < xzdeltaR / h6:
            right += 1
            if po > min_intense:
                vYstart.append(Ystart + j / i * h6)
                vZstart.append(Zstart + k / i * h6)
                vXstart.append(Xmax)
                power.append(po * reflex_factor)
                x.append(-i)
                y.append(j)
                z.append(k)

    counts, xedges, yedges, Image = plt.hist2d(xground, yground, bins, weights=final_power)
    return counts


def count_gini(distrib_list, is_show=False):
    my_list = [abs(i) for i in distrib_list]
    sorted_list1 = sorted(my_list)
    total_wealth = sum(sorted_list1)
    pop_size = len(sorted_list1)
    ginni_coef = 0
    for i in range(pop_size):
        ginni_coef += (2 * (i + 1) - pop_size - 1) * sorted_list1[i]
    ginni_coef /= ((pop_size - 1) * total_wealth)
    if is_show:
        lorenz_curve = []
        sorted_list = [i / total_wealth for i in sorted_list1]
        lorenz_curve.append(sorted_list[0])
        for i in range(1, pop_size):
            lorenz_curve.append(lorenz_curve[i - 1] + sorted_list[i])
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
        average = total_wealth / pop_size
        normed_list = [i / average for i in my_list]
        ax1.hist(normed_list, 100, normed=True)
        ax1.set_title('Normalized distribution histogram')
        ax1.set_xlabel('value/average')
        ax1.set_ylabel("normalized count")

        x = linspace(0, 1, pop_size)
        ax2.plot(x, lorenz_curve, x, x)
        ax2.set_ylim([0, 1])
        ax2.set_xlim([0, 1])
        ax2.set_title('Lorenz curve, Ginny coef. = %s' % str(round(ginni_coef, 2)))
        ax2.set_xlabel("Cumulative part")
        ax2.set_ylabel("Cumulative value")
        plt.show()
    return ginni_coef


def add_ball(matrix, size, X, Y, Z, rf, mi, xm, ym, zm):
    x, y, z = vector_generator(n)
    counts = add_light(x, y, z, bins=size, pXstart=X, pYstart=Y, pZstart=Z, reflex_factor=rf, min_intense=mi, Xmax=xm,
                       Ymax=ym, Zmax=zm)
    for i in range(size):
        for j in range(size):
            matrix[i][j] += counts[i][j]

if __name__ == '__main__':

    n = 100
    xsize = 3.6
    ysize = 3.6
    zsize = 0.6

    size = 100
    light = [[0 for i in range(size)] for j in range(size)]

    pi_space = linspace(0, PI * 2, 1)
    x_ball_start = [0.9, 0.9, 0.9, 1.8, 1.8, 1.8, 2.7, 2.7, 2.7]
    y_ball_start = [0.9, 1.8, 2.7, 0.9, 1.8, 2.7, 0.9, 1.8, 2.7]
    R = 0.89
    accu = 2000
    for q, w in zip(x_ball_start, y_ball_start):
        for i in range(accu):
            add_ball(light, size, q + R * sin(i / accu * PI * 2), w + R * cos(i / accu * PI * 2), 0.05, 0.0, 0.1, xsize,
                     ysize, zsize)
    vect = []
    for column in light:
        for i in column:
            vect.append(i)
    gini = count_gini(vect, is_show=False)

    plt.matshow(light)
    plt.colorbar()
    plt.show()
