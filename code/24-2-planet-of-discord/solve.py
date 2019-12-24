#!/usr/bin/env python -OO
import io
import math
import paivlib as paiv


def solve(text, times=200):
    grid = dict(((0, y, x), True)
        for y, s in enumerate(text.strip().splitlines())
        for x, c in enumerate(s)
        if c not in '.?')

    zones = build_zones()

    def zone(p):
        z, y, x = p
        return [(z+dz, dy, dx) for dz, dy, dx in zones[y,x]]

    def live(grid, p):
        n = sum(grid.get(i, 0) for i in zone(p) if i != p)
        return (n == 1) or (not grid.get(p) and n == 2)


    for _ in range(times):
        update = set(i for p in grid for i in zone(p))
        grid = dict((p, True) for p in update if live(grid, p))

    paiv.trace(dump(grid))
    return sum(grid.values())


def build_zones():
    wasd = ((-1, 0), (0, -1), (1, 0), (0, 1))

    def norm(y, x, ty, tx):
        if x < 0:
            return [(-1, 2, 1)]
        elif x > 4:
            return [(-1, 2, 3)]
        elif y < 0:
            return [(-1, 1, 2)]
        elif y > 4:
            return [(-1, 3, 2)]
        elif x == y == 2:
            if tx > 0:
                return [(1, i, 0) for i in range(5)]
            elif tx < 0:
                return [(1, i, 4) for i in range(5)]
            elif ty > 0:
                return [(1, 0, i) for i in range(5)]
            elif ty < 0:
                return [(1, 4, i) for i in range(5)]
        else:
            return [(0, y, x)]

    zones = dict()
    for y in range(5):
        for x in range(5):
            ps = [(0,y,x)]
            for ty,tx in wasd:
                ps.extend(norm(y+ty, x+tx, ty, tx))
            zones[y,x] = ps
    return zones


def dump(grid, level=0):
    chars = '.#'
    so = io.StringIO()
    so.write(f'\n')
    so.write(f'Depth {level}:\n')
    for y in range(5):
        for x in range(5):
            c = '?' if (y == x == 2) else chars[grid.get((level, y, x), 0)]
            so.write(c)
        so.write('\n')
    return so.getvalue().rstrip('\n')


def test():
    paiv.test_subject(solve)

    s = """
....#
#..#.
#.?##
..#..
#....
"""
    paiv.test(s, 10) == 99


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
