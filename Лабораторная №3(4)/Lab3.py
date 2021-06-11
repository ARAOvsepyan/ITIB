import itertools
from math import exp
import matplotlib.pyplot as plt


def fun(x):
    return int((((x[0] + x[1] + x[2]) % 2) * ((x[1] + x[2] + x[3]) % 2)))


def f4(net):
    if 0.5 * (net / (1 + abs(net)) + 1):
        return 1
    else:
        return 0


def f_net(x, v, v0):
    net = v0
    for (i, j) in zip(x, v):
        net += i*j
    return net


def print_table(first, name):
    print('\n|||||||||||||||||||||||||||\n')
    print(name, ': ')
    for (i, j) in zip(first, range(len(first))):
        print(name[-1], j, '->', i,)


def y_net(net):
    return 1 if net >= 0 else 0


def start(nj, c, x, X, f):
    l = 0
    v = [0] * (len(c) + 1)
    error = 1
    massive_errors = []
    massive_epochs = []
    massive_v = []
    while error > 0:
        error = 0
        massive_v.append(v.copy())
        for _ in x:
            qf = []
            for k in range(len(c)):
                s = 0
                for (i, j) in zip(_, c[k]):
                    s -= (i - j) ** 2
                qf.append(exp(s))

            y = f(f_net(qf, v[1:], v[0]))
            b = fun(_) - y
            for i in range(len(v)):
                if i == 0:
                    v[i] += b * nj
                else:
                    v[i] += b * nj * qf[i - 1]

        massive_epochs.append(l)

        for _ in X:
            qf = []
            for k in range(len(c)):
                s = 0
                for (i, j) in zip(_, c[k]):
                    s -= (i - j) ** 2
                qf.append(exp(s))

            y = f(f_net(qf, v[1:], v[0]))
            b = fun(_) - y
            error += abs(b)

        massive_errors.append(error)
        if error == 0:
            massive_v.append(v)
        l += 1
        if l > 100:
            return False

    answer = [massive_v, massive_epochs, massive_errors, c, x]
    return answer


class Neural:
    def __init__(self, nj, X, c, f):
        answer = []
        x = ([0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0],
             [1, 0, 0, 1], [1, 0, 1, 1], [1, 1, 1, 1])
        get = start(nj, c, x, X, f)
        if get:
            answer.append(get)
        print_table(answer[-1][4], 'X')
        print_table(answer[-1][0][-1], 'Весовые коэффициенты  V')
        print_table(answer[-1][3], 'C')

        print('----------------------------------------------------------------------')
        print('|', '%-7s' % 'epochs', '|', ' V', ' ' * 33, '|', '%-7s' % 'errors', '|')
        print('----------------------------------------------------------------------')
        for (i, j, k) in zip(answer[-1][0], answer[-1][1], answer[-1][2]):
            print('|', '%-7s' % j, end='')
            for t in i:
                print('|', '%-7s' % round(t, 4), end=' ')
            print('|', '%-7s' % k, '|')
        print('----------------------------------------------------------------------')

        _, ax = plt.subplots()
        ax.plot(answer[-1][1], answer[-1][2], label='суммарная ошибка')
        ax.legend()
        plt.title(f'График суммарной ошибки НС по эпохам обучения')  # заголовок
        plt.xlabel("Эпохи")  # ось абсцисс
        plt.ylabel("Ошибки")  # ось ординат
        plt.grid()  # включение отображение сетки

        plt.show()


if __name__ == '__main__':
    X = [
        [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
        [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]
    ]
    f0 = []
    f1 = []
    fs = []
    for k in X:
        fs.append(fun(k))
        if fun(k) == 1:
            f1.append(k)
        else:
            f0.append(k)

    c = []
    if len(f1) > len(f0) != 0:
        c = f0
    else:
        c = f1

    n1 = Neural(0.3, X, c, y_net)
