import numpy as np


def floyd(a, p):
    """
    Compute the epoch of a under p.
    """
    t = p[a]
    h = p[p[a]]
    i = 1
    while t != h:
        i += 1
        t = p[t]
        h = p[p[h]]
    return i


n = 100
N = 1000
epochs = np.zeros([N, n])
for i in range(N):
    p = np.random.randint(0, n, n)
    for a in range(n):
        epochs[i, a] = floyd(a, p)
print("Mean: ", np.mean(epochs))

# TODO: Make some graphics.
