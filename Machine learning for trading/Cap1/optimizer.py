import pandas as pd
import matplotlib.pyplot as pyplot
import numpy as np
import scipy.optimize as spo

# optimize an objective function using scipy


def f(X):
    Y = (X - 1.5)**2 + 0.5
    print("X = {} Y = {}".format(X, Y))
    return Y


def test_run():
    Xguess = 2.0
    min_result = spo.minimize(
        f, Xguess, method="SLSQP", options={"disp": True})
    print("Minima found at:")
    print("X = {} Y = {}".format(min_result.x, min_result.fun))

    if __name__ == "__main__":
        test_run()
