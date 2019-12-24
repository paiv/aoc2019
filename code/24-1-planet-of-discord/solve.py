#!/usr/bin/env python
import io
import time
import paivlib as paiv


def solve(text):
    grid = dict((x+1j*y, c != '.')
        for y, s in enumerate(text.strip().splitlines())
        for x, c in enumerate(s))

    visited = set()
    wasd = (-1j, -1, 1j, 1)

    def live(grid, p, x):
        n = sum(grid.get(p+i, 0) for i in wasd)
        return (n == 1) or (not x and n == 2)

    while True:
        paiv.trace(dump(grid))
        k = tuple(p for p, c in grid.items() if c)
        if k in visited: break
        visited.add(k)
        grid = dict((p, live(grid, p, c)) for p, c in grid.items())

    paiv.trace(dump(grid))
    return checksum(grid)


def checksum(grid):
    return sum(2**(int(p.real + 5 * p.imag)) for p, c in grid.items() if c)


def dump(grid):
    chars = '.#'
    so = io.StringIO()
    so.write('\n')
    xs = [int(p.real) for p in grid] or [0]
    ys = [int(p.imag) for p in grid] or [0]
    for y in range(min(ys), max(ys) + 1):
        p = 1j * y
        for x in range(min(xs), max(xs) + 1):
            c = chars[grid.get((p+x), 0)]
            so.write(c)
        so.write('\n')
    return so.getvalue().rstrip('\n')


def test():
    paiv.test_subject(solve)

    s = """
....#
#..#.
#..##
..#..
#....
"""
    paiv.test(s) == 2129920


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
