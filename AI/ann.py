import numpy as np


class ANN:
    def __init__(self, dim=[1], alfa=0.1):
        # dim excluding data dim
        self.dim = dim
        self.neurons = []
        self.add_neurons()

    def add_neurons(self):
        prev = []
        for num in self.dim:
            act = []
            for _ in range(num):
                act.append(Neuron())
            for n_0 in prev:
                for n_1 in act:
                    den = Dendrite(n_0, n_1)
                    n_0.childs.append(den)
                    n_1.fathers.append(den)
            prev = act

    def add_data(self, data):
        self.neurons[0].value = self.normalize(data)

    def train(self):
        pass

    def test(self):
        pass

    def normalize(self, data):
        mx = np.max(data)
        mn = np.min(data)
        return (data - mn) / (mx - mn)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


class Neuron:

    pass


class Dendrite:

    pass
