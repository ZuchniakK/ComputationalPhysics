__author__ = 'Konrad'
import numpy
from matplotlib.pylab import *


def NtoNsqrt(A):
    size_a = len(A)
    print(size_a ** 2)
    asqrt = numpy.zeros((size_a ** 2, size_a ** 2))
    for k in range(size_a):
        asqrt[k, k] = 1
        asqrt[size_a * (size_a - 1) + k, size_a * (size_a - 1) + k] = 1
        asqrt[size_a * k, size_a * k] = 1
        asqrt[size_a * k + (size_a - 1), size_a * k + (size_a - 1)] = 1

    for k in range(size_a - 2):
        for l in range(size_a - 2):
            i, j = k + 1, l + 1
            asqrt[i * size_a + j, i * size_a + j] = 1 + 2 * alfa
            asqrt[i * size_a + j, (i + 1) * size_a + j] = -alfa / 2
            asqrt[i * size_a + j, (i - 1) * size_a + j] = -alfa / 2
            asqrt[i * size_a + j, i * size_a + j + 1] = -alfa / 2
            asqrt[i * size_a + j, i * size_a + j - 1] = -alfa / 2
    return asqrt


def init_grid(Tp, To, Tc, N):
    grid = [[] for i in range(N)]
    for i in range(N):
        for j in range(N):
            grid[i].append(Tp)
        grid[i][0] = Tc
    return numpy.matrix(grid)


def VectorT(tempgrid, To, Tc):
    size_grid = len(tempgrid)
    vector = [0 for i in range(size_grid ** 2)]
    for k in range(size_grid - 2):
        vector[k + 1] = tempgrid[1, k + 1] + trans * (To - tempgrid[0, k + 1])
        vector[size_grid ** 2 - 2 - k] = tempgrid[size_grid - 2, size_grid - k - 1] + trans * (
            To - tempgrid[size_grid - 1, size_grid - k - 1])
    for k in range(size_grid):
        vector[size_grid * k] = Tc
        vector[size_grid * k + (size_grid - 1)] = tempgrid[k, size_grid - 2] + trans * (To - tempgrid[k, size_grid - 1])
    for k in range(size_grid - 2):
        for l in range(size_grid - 2):
            i, j = k + 1, l + 1
            vector[i * size_grid + j] = (1 - 2 * alfa) * tempgrid[i, j] + alfa * (
                tempgrid[i + 1, j] + tempgrid[i - 1, j] + tempgrid[i, j + 1] + tempgrid[i, j - 1]) / 2
    return numpy.matrix(vector)


def VectToNewGrid(tempvec, N):
    new_grid = numpy.zeros((N, N))
    for i in range(N):
        for j in range(N):
            new_grid[i, j] = tempvec[i * N + j]
    return numpy.matrix(new_grid)


if __name__ == '__main__':
    alfa = 0.5
    trans = 0.1

    grid1 = init_grid(10, 0, 20, 5)
    equation_matrix = NtoNsqrt(grid1)
    vector1 = VectorT(grid1, 5, 10)
    x = numpy.linalg.solve(equation_matrix, vector1.transpose())
    grid2 = VectToNewGrid(x, 5)

    N = 20
    Tstart = 10
    Tzr = 30
    Toto = 0
    grid1 = init_grid(Tstart, Toto, Tzr, N)
    equation_matrix = NtoNsqrt(grid1)

    for calculation_time in range(100):
        vector1 = VectorT(grid1, Toto, Tzr)
        x = numpy.linalg.solve(equation_matrix, vector1.transpose())
        grid1 = VectToNewGrid(x, N)

    plt.imshow(grid1)
    plt.colorbar()
    plt.title('Heat diffusion')
    plt.show()
