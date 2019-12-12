#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text, steps=1000):
    pos = paiv.parse_ints(text.strip())
    vel = [[0, 0, 0] for _ in pos]

    for _ in range(steps):

        for i, a in enumerate(pos):
            for b in pos:
                for u, (x, y) in enumerate(zip(a, b)):
                    vel[i][u] += 1 if x < y else -1 if x > y else 0
        pos = [[(x+u) for x, u in zip (p,v)] for p,v in zip(pos, vel)]

    def erg(p): return sum(map(abs, p))
    E = sum(erg(p)*erg(v) for p,v in zip(pos, vel))
    return E


def test():
    paiv.test_subject(solve)

    s = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
    paiv.test(s, 10) == 179

    s = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""
    paiv.test(s, 100) == 1940


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
