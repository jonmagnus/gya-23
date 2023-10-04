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

graph = graphviz.Digraph(engine="neato")
n = 113
# NOTE: Most elements are principal roots, so you can just check that
# a ** ((p - 1) // 2) == -1 for a random number.
g = 5
assert (g ** 56) % n == n - 1
a = np.random.randint(2, n - 2)
print("Alice's secret: ", a)
# We want to compute the discrete logarithm of q over g, i.e. d.
q = (g ** a) % n
p = np.zeros(n, dtype=int)
for i in range(n):
    if i <= n // 3:
        p[i] = (i * q) % n
    elif i <= 2 * n // 3:
        p[i] = (i * i) % n
    else:
        p[i] = (i * g) % n

epoch = floyd(1, p)
u = 1
a1 = 0
b1 = 0
for _ in range(epoch):
    if u <= n // 3:
        a1 += 1
    elif u <= 2 * n // 3:
        a1 *= 2
        b1 *= 2
    else:
        b1 += 1
    u = p[u]
assert ((q ** a1) * (g ** b1) - u) % n == 0
a2 = a1
b2 = b1
u_ = u
for _ in range(epoch):
    if u <= n // 3:
        a2 += 1
    elif u <= 2 * n // 3:
        a2 *= 2
        b2 *= 2
    else:
        b2 += 1
    u = p[u]
assert u_ == u, f"u {u}, u_ {u_}"
assert ((q ** a1) * (g ** b1) - (q ** a2) * (g ** b2)) % n == 0


def extended_gcd(a, b):
    if a == 0:
        if b == 0:
            return (0, 0, 0)
        else:
            return (0, 1, b)
    if b == 0:
        return (1, 0, a)
    c = a // b
    r = a - c * b
    (k, l, d) = extended_gcd(b, r)
    # k * b + l * (a - c * b) = d
    return (l, k - l * c, d)


(k, l, d) = extended_gcd(a1 - a2, n - 1)
# Choose representatives such that k and d are positive.
assert k * (a1 - a2) + l * (n - 1) == d
if d < 0:
    d = -d
    k = -k
    l = -l
if k < 0:
    c = k * d // (n - 1)
    k = k - c * (n - 1) // d
    l = l + c * (a1 - a2) // d
assert k * (a1 - a2) + l * (n - 1) == d

a2 %= n - 1
a1 += n - 1

t1, t2 = np.remainder(q ** ((a1 - a2) * k), n), np.remainder(q ** d, n)
assert t1 == t2, f"t1 {t1}, t2 {t2}"
t6 = np.remainder(q ** a1 * g ** b1, n)
t7 = np.remainder(q ** a2 * g ** b2, n)
assert t6 == t7, f"t6 {t6}, t7 {t7}"
t4 = np.remainder(q ** (a1 - a2), n)
assert np.remainder(g ** (n - 1), n) == 1
t5 = np.remainder(g ** (b2 - b1), n)
assert t4 == t5, f"t4 {t4}, t5 {t5}"
t3 = np.remainder(g ** ((b2 - b1) * k), n)
assert t2 == t3, f"t2 {t2}, t3 {t3}"
theta = g ** ((n - 1) // d) % n
a_ = (b2 - b1) * k // d
gbase = (g ** a_) % n
for i in range(d):
    if (gbase - q) % n == 0:
        a_ = (a_ + i * (n - 1) // d) % (n - 1)
        break
    gbase = (gbase * theta) % n
assert a_ == a, f"a {a}, a_ {a_}"


# p = np.random.randint(0, n, n)
# p = np.random.permutation(n)
tail, cycle = find_rho(1, p)
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
