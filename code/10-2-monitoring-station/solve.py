#!/usr/bin/env python -OO
import itertools
import math
import paivlib as paiv
from collections import defaultdict


def solve(text):
    grid = [(x, y)
        for y, s in enumerate(text.strip().splitlines())
        for x, q in enumerate(s)
        if q == '#']

    lines = defaultdict(set)
    for i, a in enumerate(grid):
        for j, b in enumerate(grid[i:]):
            lines[a].add(angle(a, b))
            lines[b].add(angle(b, a))

    n = max(map(len, lines.values()))
    for p, v in lines.items():
        if len(v) == n:
            pos = p
            break
    else: return 'poop'

    paiv.trace('X:', pos)

    xs = sorted((angle(pos, a), paiv.l2_dist(pos, a), a) for a in grid if a != pos)
    gs = [[p[2] for p in g] for k, g in itertools.groupby(xs, key=lambda p: p[0])]

    def shred(gs):
        while gs:
            for g in gs: yield g[0]
            gs = [g[1:] for g in gs if len(g) > 1]

    x, y = next(itertools.islice(shred(gs), 199, 200))
    return x * 100 + y


def angle(a, b):
    ax, ay = a
    bx, by = b
    g = math.atan2(by - ay, bx - ax)
    g = (math.pi / 2 + g) % (2 * math.pi)
    return round(g, 8)


def test():
    paiv.test_subject(solve)

    s = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    paiv.test(s) == 802


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
