#!/usr/bin/env python -OO
import heapq
import paivlib as paiv
from collections import defaultdict, deque


def solve(text):
    orbits = dict(s.split(')')[::-1] for s in text.splitlines())

    links = defaultdict(set)
    for k,v in orbits.items():
        links[k].add(v)
        links[v].add(k)

    def dist(start, goal):
        visited = set()
        fringe = deque()
        fringe.append((0, start))
        while fringe:
            steps, pos = fringe.popleft()
            if pos in visited: continue
            visited.add(pos)
            if pos == goal: return steps
            for n in links[pos]:
                fringe.append((1 + steps, n))

    return dist('YOU', 'SAN') - 2


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
K)YOU
I)SAN
""".strip()
    paiv.test(s) == 4


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
