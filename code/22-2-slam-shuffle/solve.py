#!/usr/bin/env python
import itertools
import paivlib as paiv


def solve(text, m=119315717514047, t=101741582076661, q=2020):

    def simplify(text):
        a = 1
        b = 0

        for op in text.strip().splitlines():
            arg = op.split()[-1]

            if op.startswith('deal with'):
                v = int(arg)
                a = a * v % m
                b = b * v % m

            elif op.startswith('deal into'):
                a = -a % m
                b = -(b + 1) % m

            elif op.startswith('cut'):
                v = int(arg)
                b = (b - v) % m

        return (a, b)

    a, b = simplify(text)

    # affine transform, augmented matrix:
    #   a b
    #   0 1
    a, b, *_  = mpow((a, b, 0, 1), t, m)

    # Ax+B = q mod m
    # x = ((q - B) mod m) * modinv(A, m)

    x = (q - b) * modinv(a, m) % m
    return x


# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers
def modinv(n, mod):
    t, w, r = 0, 1, mod
    while n:
        (q, n), r = divmod(r, n), n
        t, w = w, t - q * w
    if r > 1: raise Exception('not invertible ' + repr(n))
    if t < 0: t += mod
    return t


def mmul(a, b, mod):
    return (
        (a[0] * b[0] + a[1] * b[2]) % mod,
        (a[0] * b[1] + a[1] * b[3]) % mod,
        (a[2] * b[0] + a[3] * b[2]) % mod,
        (a[2] * b[1] + a[3] * b[3]) % mod)


def mpow(base, exp, mod):
    ans = (1, 0, 0, 1)
    while exp > 0:
        exp, t = divmod(exp, 2)
        if t:
            ans = mmul(ans, base, mod)
        base = mmul(base, base, mod)
    return ans


def test():
    paiv.test_subject(solve)

    s = """
deal with increment 7
deal into new stack
deal into new stack
"""
    for i, x in enumerate([0,3,6,9,2,5,8,1,4,7]):
        paiv.test(s, 10, 1, i) == x

    s = """
cut 6
deal with increment 7
deal into new stack
"""
    for i, x in enumerate([3,0,7,4,1,8,5,2,9,6]):
        paiv.test(s, 10, 1, i) == x

    s = """
deal with increment 7
deal with increment 9
cut -2
"""
    for i, x in enumerate([6,3,0,7,4,1,8,5,2,9]):
        paiv.test(s, 10, 1, i) == x

    s = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
    for i, x in enumerate([9,2,5,8,1,4,7,0,3,6]):
        paiv.test(s, 10, 1, i) == x


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
