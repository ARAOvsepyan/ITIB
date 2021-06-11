from matplotlib import pyplot as plt
from numpy import tanh

class NN:
    def __init__(self, foo, border, d, maxEpoch=30):
        self.W = [0] * 5
        self.t = [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
        self.Rate = 0.3

        self.epoch = 0

        self.x = [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1]
        ]
        self.stable = [i for i in range(16)]

        self.foo = foo
        self.border = border
        self.d = d

        self.maxEpoch = maxEpoch

    def kick(self):
        cont = True
        while cont:
            stable = self.stable.copy()
            res = False
            for i in range(len(self.stable)):
                del(self.stable[i])
                res = self.work(visible=False)

                if res:         # got result 
                    break
                if not res:     # no res -> reset 
                    self.W = [0] * 5
                    self.stable = stable.copy()

            if not res:
                cont = False
            else:
                output = f'''------------------------------------------------------------------
Всего Эпох: {res['epochs']}
Номера используемых векторов  = {self.stable}'''
                output += '\nКонченые веса = '
                for w in self.W:
                    output += str(round(w, 2)) + ' '
                self.W = [0] * 5
                print(output)

    def work(self, visible=True):
        self.epoch = 0
        E = 1
        self.errors = []
        while (E > 0):
            if (self.epoch > self.maxEpoch):
                return False

            if visible:
                print(f'''
---------------------------------
        Эпоха: {self.epoch}
---------------------------------''')
            E = self.tick(visible)
            self.errors.append(E)
            self.epoch += 1

        return {'epochs' : self.epoch - 1, 'weights' : self.W}

    def tick(self, visible=True):
        y = [0] * 16

        y_K = [0] * 16
        w_K = self.W.copy()

        for ROW in self.stable:
            x = self.x[ROW]

            net = self.W[0]
            net_K = w_K[0]
            for i in range(len(x)):
                net += x[i] * self.W[i+1]
                net_K += x[i] * w_K[i+1]

            out = int(self.foo(net) >= self.border)
            out_K = int(self.foo(net_K) >= self.border)

            y[ROW] = out
            y_K[ROW] = out_K


            self.correctWeights(x, y[ROW], self.t[ROW], d=self.d(net))

        output = 'y = '
        for i in y_K:
            output += str(i) + ' '

        output += '\nW = '
        for w in self.W:
            output += str(round(w, 2)) + '  '

        E = self.dist(y_K)
        output += '\nE = ' + str(E)
        if visible:
            print(output, end='')
        return E

    def correctWeights(self, x, y, t, d):
        x = [1] + x
        for i in range(len(self.W)):
            self.W[i] += self.Rate * (t - y) * x[i] * d

    def dist(self, y_K):
        e = 0
        for i in range(len(y_K)):
            e += abs(self.t[i] - y_K[i]) 
        return e

    def graph(self, f_name):
      plt.plot([k for k in range(self.epoch)], self.errors)
      plt.grid()
      plt.xlabel('epochs')
      plt.ylabel('errors')
      plt.savefig(f'{f_name}.png')
    #   plt.show()



def threshold(net):
    return net

def thr_d(net):
    return 1

def logistic(net):
    return 0.5*(net/(1+abs(net)) + 1)

def log_d(net):
    return 2/((2+2*abs(net))**2)



print('''t = 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1\n''')

print('''
=================================
            Пороговая
=================================''', end='')
nn_thr = NN(threshold, 0, thr_d)
res_thr = nn_thr.work(visible=True)
nn_thr.graph('threshold')


print('''
=================================
            Логистическая
=================================''', end='')
nn_log = NN(logistic, 0.5, log_d)
res_log = nn_log.work(visible=True)
nn_log.graph('logistic')


print('''
=================================
    Минимальный набор векторов
        Пороговая ФА
=================================''')
nn_min = NN(threshold, 0, thr_d, maxEpoch=res_thr['epochs'])
nn_min.kick()


print('''
=================================
    Минимальный набор векторов
        Логистическая ФА
=================================''')
nn_min = NN(logistic, 0.5, log_d, maxEpoch=res_log['epochs'])
nn_min.kick()
