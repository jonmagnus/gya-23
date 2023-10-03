import random


def fast_exp_mod(a, b, m):
    c = 1
    while b != 0:
        if b % 2 != 0:
            c = (c * a) % m
        a = (a * a) % m
        b //= 2
    return c


def miller_rabin(p, k):
    if p < 2:
        return False
    if p == 2:
        return True
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, p - 2)
        # x = (a ** d) % p
        x = fast_exp_mod(a, d, p)
        for _ in range(s):
            y = (x ** 2) % p
            if y == 1 and x != 1 and x != p - 1:
                return False
            x = y
        if y != 1:
            return False
    return True


prime = 2 ** 255 - 19
print(f"{prime} is prime: {miller_rabin(prime, 1000)}")
