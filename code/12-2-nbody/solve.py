#!/usr/bin/env python -OO
import math
import paivlib as paiv


def solve(text):
    pos = paiv.parse_ints(text.strip())

    pos = [*zip(*pos)]
    ans = 1

    for p in pos:
        v = [0 for _ in p]
        n = 0
        while n == 0 or any(v):
            for i, x in enumerate(p):
                for y in p:
                    v[i] += 1 if x < y else -1 if x > y else 0
            p = [(x+u) for x,u in zip(p, v)]
            n += 1
        ans *= n

    return ans


def test():
    paiv.test_subject(solve)

    s = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
    paiv.test(s) == 2772

    s = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""
    # paiv.test(s) == 4686774924


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
