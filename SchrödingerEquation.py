import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
import math


def fillmat(n, value, level=1):
    if level == 1:
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i].append(-2 * value)
                elif abs(i - j) == 1:
                    A[i].append(value)
                else:
                    A[i].append(0)
    elif level == 2:
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i].append(-5 / 2 * value)
                elif abs(i - j) == 1:
                    A[i].append(4 / 3 * value)
                elif abs(i - j) == 2:
                    A[i].append(-1 / 12 * value)
                else:
                    A[i].append(0)
    elif level == 4:
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i].append(-205 / 72 * value)
                elif abs(i - j) == 1:
                    A[i].append(8 / 5 * value)
                elif abs(i - j) == 2:
                    A[i].append(-1 / 5 * value)
                elif abs(i - j) == 3:
                    A[i].append(8 / 315 * value)
                elif abs(i - j) == 4:
                    A[i].append(-1 / 560 * value)
                else:
                    A[i].append(0)


def get_analitical_eigenvalues(n, L):
    return math.pi ** 2 * n ** 2 / (2 * L ** 2 * 18.8972 ** 2) / 0.03649


def get_analitical_eigenfunc(n, L, vectorsize):
    A = math.sqrt(2 / (L * 18.8972))
    k = n * math.pi / L
    x = np.linspace(0, L, vectorsize)
    vector = [A * math.sin(k * i) for i in x]
    return vector


def findnminindex(originaltab, n):
    tab = [i for i in originaltab]
    maxvalue = max(tab)
    for i in range(n):
        value = maxvalue
        iterator = 0
        minindex = 0
        for element in tab:
            if element <= value:
                minindex = iterator
                value = element
            iterator += 1
        if i < n - 1:
            tab[minindex] = maxvalue
        else:
            return minindex


def get_zero(tab):
    newtab = [0 for i in range(len(tab) + 2)]
    for i in range(n - 2):
        newtab[i + 1] = tab[i]
    return newtab


if __name__ == '__main__':

    # Constants:
    nm = 18.8972
    eV = 0.03649
    Lnm = 5
    L = Lnm * nm
    n = 500
    dx = L / n
    a = -1 / (2 * dx ** 2)

    A = [[] for i in range(n - 2)]
    level = 4
    fillmat(n - 2, a, level)
    w, v = la.eigh(A)
    w = w / eV
    y = [math.sqrt(i) for i in w]
    x = []
    for i in range(len(w) + 2):
        x.append(Lnm * i / n)
    plt.title("Wave function")
    for element in range(1, 4):

        plt.subplot(3, 1, element)
        teoreticalvector = get_analitical_eigenfunc(element, Lnm, n)
        minindex = findnminindex(w, element)
        eigfunc = [-v[i][minindex] * math.sqrt(n) / 10 for i in range(len(v))]
        eigfunc = get_zero(eigfunc)

        if element == 2 or element == 3:
            eigfunc = [-i for i in eigfunc]
        if element == 1:
            plt.title("Wave function, dx = %s nm, approximation level = %s" % (Lnm / n, level))
        plt.plot(x, eigfunc, x, teoreticalvector)
        plt.legend(["computed", "analitical"])
        plt.xlabel("nm")
    plt.show()
    theor = [get_analitical_eigenvalues(i + 1, 5) for i in range(3)]
    squareerror = 0
    for i in range(3):
        squareerror += ((theor[i] - w[i]) ** 2) / 3

    potential = [0 for i in range(n - 2)]
    for i in range(n - 2):
        if i >= 0.35 * n and i <= 0.65 * n:
            potential[i] = -0.5
    for i in range(n - 2):
        A[i][i] += potential[i]

    w, v = la.eigh(A)
    w = sorted(w)
    x = []
    for i in range(len(w)):
        x.append(-Lnm + 2 * Lnm * i / n)

    plt.title("Wave function")
    for element in range(1, 4):
        plt.subplot(4, 1, element)
        minindex = findnminindex(w, element)
        eigfunc = [-v[i][minindex] * math.sqrt(n) / 10 for i in range(len(v))]
        if element == 1:
            eigfunc = [-i for i in eigfunc]
            plt.title("Wave function, dx = %s nm, aproximation level = %s" % (Lnm / n, level))
        plt.plot(x, eigfunc)
        plt.xlabel("nm")
    plt.subplot(4, 1, 4)
    plt.plot(x, potential)
    plt.xlim(min(x), max(x))
    plt.ylim(min(potential) - 0.5, max(potential) + 0.5)
    plt.xlabel("nm")
    plt.ylabel("Potential eV")
    plt.show()
