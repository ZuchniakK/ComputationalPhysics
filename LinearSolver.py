class InputReader:
    eq = []

    def __init__(self):
        tmp = 1
        while tmp:
            self.size = input("enter linear equation order, or enter 'file' to read data from file")
            if self.size.lower() == "file":
                tmp = 1
                while tmp:
                    from tkinter import Tk
                    from tkinter.filedialog import askopenfilename
                    from numpy import loadtxt
                    try:
                        Tk().withdraw()
                        filename = askopenfilename()
                        self.eq = loadtxt(filename)
                    except ValueError:
                        print("Bad file structure")
                    except FileNotFoundError:
                        print("File not choose")
                    else:
                        if len(self.eq[0]) - len(self.eq) == 1:
                            tmp = 0
                        else:
                            print("Size of numbers in the rows does not match the amount of lines")
                print(self.eq)
                tmp = 0
                self.size = len(self.eq)
            elif self.size.isnumeric():
                self.size = int(self.size)
                if self.size > 0:
                    tmp = 0
                    for i in range(self.size):
                        self.eq.append([])
                        for j in range(self.size + 1):
                            self.eq[i].append(
                                input("Enter  element X%s , %s equation" % (str(self.size - j), str(i + 1))))
                else:
                    print(">0")

    def show(self):
        print(self.eq)

    def get_eq(self):
        return self.eq

    def __del__(self):
        if isinstance(self.eq, list):
            self.eq.clear()


class InputValidator:
    ve1 = []
    free = []
    error = 0

    def __init__(self, eq1):
        iterator = 0
        if isinstance(eq1, list):
            for elem in eq1:
                self.ve1.append([])
                k = len(elem)
                for i in elem:

                    if i.isnumeric():
                        if k > 1:
                            self.ve1[iterator].append(int(i))
                        else:
                            self.free.append(int(i))
                    else:
                        print("Not a number")
                        self.error = 1
                        break
                    k -= 1
                iterator += 1
        else:
            for elem in eq1:
                self.ve1.append([])
                k = len(elem)
                for i in elem:
                    if k > 1:
                        self.ve1[iterator].append(int(i))
                    else:
                        self.free.append(int(i))
                    k -= 1
                iterator += 1

    def __del__(self):
        self.ve1.clear()
        self.free.clear()
        self.error = 0

    def show(self):
        print(self.ve1)
        print(self.free)

    def get_eq(self):
        return self.ve1

    def get_free(self):
        return self.free

    def get_error_value(self):
        return self.error


class Solver:
    score = []
    numpy_use = True

    def __init__(self, a, b, use_numpy=None):
        if use_numpy is None:
            use_numpy = self.numpy_use
        if use_numpy:
            self.score = self.use_numpy_solver(a, b)
            print("Numpy solver used")
        else:
            self.score = self.use_gauss(a, b)
            print("Gauss elimination method used")

    def get_score(self):
        return self.score

    def use_gauss(self, a, b):
        if len(a) == 2 and a[0][0] / a[0][1] == a[1][0] / a[1][1]:
            return False
        matrix_a = []
        for i in range(len(b)):
            matrix_a.append([])
            matrix_a[i].extend(a[i])
            matrix_a[i].append(b[i])
        n = len(matrix_a)

        for i in range(0, n):
            max_el = abs(matrix_a[i][i])
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix_a[k][i]) > max_el:
                    max_el = abs(matrix_a[k][i])
                    max_row = k

            for k in range(i, n + 1):
                tmp = matrix_a[max_row][k]
                matrix_a[max_row][k] = matrix_a[i][k]
                matrix_a[i][k] = tmp

            for k in range(i + 1, n):
                c = -matrix_a[k][i] / matrix_a[i][i]
                for j in range(i, n + 1):
                    if i == j:
                        matrix_a[k][j] = 0
                    else:
                        matrix_a[k][j] += c * matrix_a[i][j]

        x = [0 for i in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = matrix_a[i][n] / matrix_a[i][i]
            for k in range(i - 1, -1, -1):
                matrix_a[k][n] -= matrix_a[k][i] * x[i]
        return x

    def use_numpy_solver(self, a, b):
        if len(a) == 2 and a[0][0] / a[0][1] == a[1][0] / a[1][1]:
            return False
        from numpy.linalg import solve as podaj_wyniczek
        return podaj_wyniczek(a, b)


class ApplicationMgr:
    visualize = True

    def __init__(self, vis=None, use_numpy=None):
        if vis is None:
            vis = self.visualize

        tmp = 1
        while tmp:
            x = InputReader()
            print(x.get_eq())
            y = InputValidator(x.get_eq())

            tmp = 0
            if y.get_error_value() == 1:
                print("entered wrong parameters")
                print("enter the parameters again")
                tmp = 1
                del x
                del y

        z = Solver(y.get_eq(), y.get_free(), use_numpy)
        score = z.get_score()
        if type(score) == bool:
            print("indefinite equation")
        else:
            print(score)
            if vis:
                import matplotlib.pylab as plt
                from numpy import linspace
                if len(score) == 2:
                    parameters = y.get_eq()
                    xa, xb, ya, yb = parameters[0][0], parameters[0][1], parameters[1][0], parameters[1][1]
                    param_c = y.get_free()
                    xc, yc = param_c[0], param_c[1]
                    if score[0] >= 0:
                        area = linspace(score[0] * 0.7, score[0] * 1.4, 500)

                    else:
                        area = linspace(score[0] * 1.4, score[0] * 0.7, 500)
                    x = [xc / xb - xa / xb * i for i in area]
                    y = [yc / yb - ya / yb * i for i in area]
                    plt.plot(area, x)
                    plt.plot(area, y)
                    plt.plot(score[0], score[1], 'ro')
                    from numpy import round
                    plt.annotate('(%s,%s)' % (str(round(score[0], 2)), str(round(score[1], 2))),
                                 xy=(score[0], score[1]), xytext=(
                            (score[0] + max(area[0], area[499])) / 2, (score[1] + max(y[0], y[499], x[0], x[499])) / 2),
                                 arrowprops=dict(facecolor='black', shrink=0.05))
                    plt.show()

if __name__ == '__main__':
    k = ApplicationMgr()
