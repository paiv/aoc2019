#!/usr/bin/env python -OO
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
    return n


def angle(a, b):
    ax, ay = a
    bx, by = b
    g = math.atan2(by - ay, bx - ax)
    return round(g, 8)


def test():
    text = """
#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c
"""
    grid = [(x, y)
        for y, s in enumerate(text.strip().splitlines())
        for x, q in enumerate(s)
        if q != '.']

    lines = defaultdict(set)
    for i, a in enumerate(grid):
        for j, b in enumerate(grid[i:]):
            lines[a].add(angle(a, b))
            lines[b].add(angle(b, a))

    origin = (0, 0)

    for k in 'abcdefg':
        p, = [(x, y)
            for y, s in enumerate(text.strip().splitlines())
            for x, q in enumerate(s)
            if q == k.upper()]
        xs = [(x, y)
            for y, s in enumerate(text.strip().splitlines())
            for x, q in enumerate(s)
            if q == k.lower()]
        for x in xs:
            u = angle(origin, p)
            v = angle(origin, x)
            assert u == v, (k, p, u, x, v)


    paiv.test_subject(solve)

    s = """
.#..#
.....
#####
....#
...##
"""
    paiv.test(s) == 8

    s = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    paiv.test(s) == 33

    s = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    paiv.test(s) == 35

    s = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
    paiv.test(s) == 41

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
    paiv.test(s) == 210


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
