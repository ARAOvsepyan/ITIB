import numpy as np
from matplotlib import pyplot as plt
from random import random, sample
from math import inf

class NeuralNetwork():
    def __init__(self, x, dims, images):
        self.I = dims[0]
        self.J = dims[1]
        self.k = self.I * self.J    # размерность вектора образа
    
        self.X = x
        self.L = len(self.X)        # кол-во образов
        self.images = images

    def setWeights(self):
        self.W = np.dot(
             np.transpose([self.X[0]]),
             [self.X[0]]
        ) + np.dot(
             np.transpose([self.X[1]]),
             [self.X[1]]
        ) + np.dot(
             np.transpose([self.X[2]]),
             [self.X[2]]
        )
        np.fill_diagonal(self.W, 0)
        np.savetxt('./weights.txt', self.W, fmt='%3.0d')

    def correct(self, corrupted):
        epoch = 0
        E = inf

        prev = corrupted

        while E > 0:
            net = [0] * self.k
            y = []
            for k in range(len(prev)):
                for j in range(len(prev)):
                    net[k] += self.W[j][k] * prev[j]
                y.append(np.sign(net[k]) if net[k] != 0 else prev[k])

            E = [0 if y[k] == prev[k] else 1 for k in range(self.k)].count(1)
            prev = y

            print(f'K: {epoch} E: {E}')
            epoch += 1

        self.print(corrupted, prev)

    def print(self, corrupted, corrected):
        print(f'\nискаженный\tисправленный')
        for i in range(self.I):
            output = ''
            for j in range(self.J): 
                output += '# ' if corrupted[i + j*self.I] == 1 else '  '
            output += '\t'
            for j in range(self.J):   
                output += '# ' if corrected[i + j*self.I] == 1 else '  '
            print(output)
        print('\n' + '-'*30 + '\n')


def corrupt(original, percent):
    length = len(original)
    indexes = sample(range(length), int(length*percent/100))
    for i in indexes:
        original[i] *= -1
    return original
    

def main():
    dims = 6, 4         # высота X ширина образа
    images = (2, 4, 6)  # правильные образы
    X : List[List[int]] = [[]] * len(images)
    X[0] = [1, -1, -1, 1, 1, 1] + [1, -1, -1, 1, -1, 1] + [1, -1, -1, 1, -1, 1] + [1, 1, 1, 1, -1, 1]       # 2
    X[1] = [-1, -1, 1, 1, -1, -1] + [-1, 1, -1, 1, -1, -1] + [1, -1, -1, 1, -1, -1] + [1, 1, 1, 1, 1, 1]    # 4
    X[2] = [-1, 1, 1, 1, 1, -1] + [1, -1, 1, -1, -1, 1] + [1, -1, 1, -1, -1, 1] + [1, -1, -1, 1, 1, -1]     # 6

    NN = NeuralNetwork(X, dims, images)
    NN.setWeights()

    corrupted = []
    percent = 20
    for _ in range(2):
        for i in range(len(images)):
            corrupted.append(corrupt(X[i].copy(), percent))

    for img in corrupted:
        NN.correct(img)


if __name__ == '__main__':
    main()