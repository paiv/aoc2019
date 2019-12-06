#!/usr/bin/env python
import paivlib as paiv


def solve(text):
    orbits = dict(s.split(')')[::-1] for s in text.splitlines())

    def level(n):
        k = orbits.get(n)
        return (1 + level(k)) if k else 0

    return sum(level(k) for k in (set(orbits) | set(orbits.values())))


def test():
    paiv.test_subject(solve)
    s = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".strip()
    paiv.test(s) == 42


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
