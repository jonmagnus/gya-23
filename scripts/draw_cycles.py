import numpy as np
import tempfile
import graphviz
from floyd import floyd


def fast_compose(p, r):
    c = np.arange(len(p))
    while r > 0:
        if r % 2 != 0:
            c = c[p]
        p = p[p]
        r //= 2
    return c


def find_rho(a, p):
    epoch = floyd(a, p)
    b = p[a]
    for _ in range(epoch):
        b = p[b]
    cycle = [b]
    b = p[b]
    while b != cycle[0]:
        cycle.append(b)
        b = p[b]
    tail = []
    cycle_index = np.remainder(-epoch - 1, len(cycle))
    while a != cycle[cycle_index]:
        tail.append(a)
        a = p[a]
        cycle_index += 1
        if cycle_index >= len(cycle):
            cycle_index -= len(cycle)
    return tail, cycle


def test_find_rho():
    n = 100
    p = np.random.permutation(n)
    for a in range(n):
        tail, cycle = find_rho(a, p)
        assert len(tail) == 0, f"{tail}\n" + f"{cycle}\n"
    p = np.random.randint(0, n, n)
    for a in range(n):
        tail, cycle = find_rho(a, p)
        assert len(np.intersect1d(tail, cycle)) == 0, (
            f"{tail}\n" + f"{cycle}\n" + f"{np.intersect1d(head, cycle)}\n"
        )


test_find_rho()


# TODO: Make an example with n a prime and the random function is pollards three cases.
# NOTE: Most elements are principal roots, so you can just check that
# a ** ((p - 1) // 2) == -1 for a random number.

n = 20
graph = graphviz.Digraph(engine="neato")
# p = np.random.randint(0, n, n)
p = np.random.permutation(n)
tail, cycle = find_rho(0, p)
for i in tail:
    graph.node(str(i), color="blue")
    graph.edge(str(i), str(p[i]), color="blue")
for i in cycle:
    graph.node(str(i), color="red")
    graph.edge(str(i), str(p[i]), color="red")
for i in range(n):
    if i not in tail and i not in cycle:
        graph.node(str(i))
        graph.edge(str(i), str(p[i]))

graph.render(tempfile.mktemp(), view=True)
