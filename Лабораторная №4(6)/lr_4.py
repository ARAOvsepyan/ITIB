from math import exp, sqrt, inf
from matplotlib import pyplot as plt
from random import random


class NeuralNetwork():
    def __init__(self, props):
        self.N = props.get('N')
        self.J = props.get('J')
        self.M = props.get('M')

        self.x = props.get('x')
        self.t = props.get('t')

        self.W_0 = [[random()] * self.J for _ in range(self.N+1)]
        self.W_1 = [[random()] * self.M for _ in range(self.J+1)]

        self.rate = 1

        self.minE = 0.001
        self.maxK = 100

    def train(self, graph=False, debug=False):
        self.K = 1
        self.E = [self.minE+1]
        while self.E[len(self.E)-1] > self.minE and self.K < self.maxK:
            print(f'\nEpoch\tError\tExit signal')

            self.E.append(self.tick(debug))
            self.K += 1

        if graph:
            self.graph()

    def tick(self, debug):
        net_0 = [self.W_0[0][j] for j in range(self.J)]    
        y_0 = [None] * self.J
        for j in range(self.J):
            for n in range(self.N):
                net_0[j] += self.W_0[n+1][j] * self.x[n+1]

            y_0[j] = self.activationFunction(net_0[j])

        net_1 = [self.W_1[0][m] for m in range(self.M)]
        y_1 = [None] * self.M
        for m in range(self.M):
            for j in range(self.J):
                net_1[m] += self.W_1[j+1][m] * y_0[j]

            y_1[m] = self.activationFunction(net_1[m])

        d_1 = [self.derivativeAF(net_1[m]) * (self.t[m] - y_1[m]) for m in range(self.M)]

        d_0 = [None] * self.J
        for j in range(self.J):
            tmp = 0
            for m in range(self.M):
                tmp += d_1[m] * self.W_1[j][m]
            d_0[j] = self.derivativeAF(net_1[m]) * tmp

        for n in range(self.N+1):
            for j in range(self.J):
                self.W_0[n][j] += self.rate * self.x[n] * d_0[j]

        net_0 = [1] + net_0
        for j in range(self.J+1):
            for m in range(self.M):
                self.W_1[j][m] += self.rate * net_0[j] *d_1[m]
        
        if debug:
            self.printWeights()

        E = 0
        for m in range(self.M):
            E += (self.t[m]-y_1[m])*(self.t[m]-y_1[m])
        E = sqrt(E)

        print(f'{self.K}\t{round(E, 4)}\t', end='')
        for y in y_1:
            print(f'{round(y, 4)} ',end='')
        print()

        return E

    def activationFunction(self, net):
        return (1-exp(-net))/(1+exp(-net))

    def derivativeAF(self, net):
        return 0.5 * (1 - self.activationFunction(net)*self.activationFunction(net))

    def printWeights(self):
        print('\nfirst layer')
        for j in range(len(self.W_0)):
            print(f'w{j}(1) = [', end='')
            for i in range(len(self.W_0[j])):
                print(round(self.W_0[j][i], 4), end='')
                if i != len(self.W_0[j])-1:
                    print(', ', end='')
            print(']')
        
        print('\nsecond layer')
        for j in range(len(self.W_1)):
            print(f'w{j}(2) = [', end='')
            for i in range(len(self.W_1[j])):
                print(round(self.W_1[j][i], 4), end='')
                if i != len(self.W_1[j])-1:
                    print(', ', end='')
            print(']')

    def graph(self):
        plt.xticks(range(self.K)[1:])
        plt.plot(range(self.K)[1:], self.E[1:], marker='o', markersize=4)
        plt.grid()
        plt.xlabel('epochs', fontsize=20)
        plt.ylabel('errors * 1000', fontsize=20)
        plt.savefig('graph.png')
        plt.show()


def main():
    NN = NeuralNetwork({
        'N' : 2,
        'J' : 1,
        'M' : 2,
        'x' : [1, 2, 2],
        't' : [0.3, 0.1]
        })
    NN.train(graph=True, debug=True)


if __name__ == '__main__':
    main()