from math import sin, cos


def func(x):
    return sin(x) + 5


def simpson(func, interval):
    x = interval[0]
    dx = interval[2] / 2
    n = int((interval[1] - interval[0]) / dx)
    result = 0
    for i in range(n // 2):
        result = result + dx / 3. * (func(x) + 4 * func(x + dx) + func(x + 2 * dx))
        x = x + 2 * dx
    return result


def rectangle(func, interval):
    x = interval[0]
    dx = interval[2]
    # x = x + dx/2
    n = int((interval[1] - interval[0]) / dx)
    result = 0
    for i in range(n):
        result = result + func(x) * dx
        x = x + dx
    return result


def trapezoid(func, interval):  # trapezoids method modified to increase speed (added former, current)
    x = interval[0]
    dx = interval[2]
    n = int((interval[1] - interval[0]) / dx)
    result = 0
    for i in range(n):
        result = result + dx * (func(x) + func(x + dx)) / 2
        x = x + dx
    return result


def manager(func, method, interval, expected_value):
    result = method(func, interval)
    error = abs(expected_value - result)
    return error


def print_plot(data, tytul, iksy, igreki):
    x = data[0]
    import matplotlib.pyplot as plt
    fig = plt.figure()

    plt.plot(x, data[1], 'r-', label='rectangle')
    plt.plot(x, data[2], 'b-', label='trapezoid')
    plt.plot(x, data[3], 'g-', label='Simpson')

    fig.autofmt_xdate()

    plt.gca().invert_xaxis()
    plt.legend(loc='upper left')
    plt.xlabel(iksy)
    plt.ylabel(igreki)
    plt.title(tytul)
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    expected_value = 26 - cos(5)
    print(manager(func, rectangle, (0, 5, .9), expected_value))
    print(manager(func, trapezoid, (0, 5, .9), expected_value))
    print(manager(func, simpson, (0, 5, .9), expected_value))

    data = []

    for i in range(10, 1000):
        onedivi = 10. / i
        rec = manager(func, rectangle, (0, 5, onedivi), expected_value)
        tra = manager(func, trapezoid, (0, 5, onedivi), expected_value)
        sim = manager(func, simpson, (0, 5, onedivi), expected_value)
        data.append((onedivi, rec, tra, sim))
        # print rec, tra, sim
    datax = []
    datarec = []
    datatra = []
    datasim = []
    for d in data:
        datax.append(d[0])
        datarec.append(d[1])
        datatra.append(d[2])
        datasim.append(d[3])
    data = [datax, datarec, datatra, datasim]
    print_plot(data, 'error vs step', 'step', 'error')
