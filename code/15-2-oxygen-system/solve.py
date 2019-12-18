#!/usr/bin/env python
import intcode as ic
import io
import paivlib as paiv
import sys
import time
from collections import defaultdict, deque


def solve(text):
    if 0:
        symb = dict(zip(' .#OS', [0, Grid.SPACE, Grid.WALL, Grid.TANK, Grid.SPACE]))
        grid = dict((x + 1j*y, symb[c]) for y, row in enumerate(text.splitlines()) for x, c in enumerate(row))
        return fill_oxygen(grid)

    image = ic.IntcodeImage.loads(text)
    vm = ic.IntcodeVM(image)

    droid = Droid(trace=True, fps=144)
    vm.run(droid)

    paiv.trace(str(droid).rstrip())

    ans = fill_oxygen(droid.grid)
    return ans


class Grid:
    SPACE = 1
    WALL = 2
    BOT = 3
    TANK = 4
    ORIGIN = 5


class Droid:
    def __init__(self, trace=False, fps=2):
        self.trace = trace
        self.fps = fps or 1
        self.grid = defaultdict(int)
        self.pos = 0
        self.plan = None
        self.grid[self.pos] = Grid.ORIGIN
        self.exploring = True

    def __str__(self):
        grid = dict(self.grid)
        #        012345
        chars = ' .#DOS'
        grid[self.pos] = Grid.BOT
        so = io.StringIO()
        xs = [int(p.real) for p in grid] or [0]
        ys = [int(p.imag) for p in grid] or [0]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                p = x + 1j * y
                c = chars[grid.get(p, 0)]
                so.write(c)
            so.write('\n')
        return so.getvalue()

    def is_active(self):
        return self.exploring

    moves = [1, 0, 2, 3, 0, 4]
    keyb = dict(zip('wasd', (-1j,-1,1j,1)))

    def read(self):
        if 0:
            t = None
            while not t:
                c = sys.stdin.read(1).rstrip()
                t = self.keyb.get(c)
            xto = self.pos + t
            self.plan = deque([xto])
            paiv.trace(c, t, xto)

        else:
            if not self.plan:
                self.plan = self._whats_the_plan(self.grid, self.pos)
                if not self.plan:
                    return 0
            xto = self.plan[0]

        x = int(4 + xto.real - self.pos.real)
        y = int(1 + xto.imag - self.pos.imag)
        t = self.moves[x] + self.moves[y]
        return t

    def write(self, value):
        xto = self.plan.popleft()
        if value == 0:
            self.grid[xto] = Grid.WALL
        elif value == 1:
            self.grid[xto] = Grid.SPACE
            self.pos = xto
        elif value == 2:
            self.grid[xto] = Grid.TANK
            self.pos = xto

        if self.trace:
            print(self)
            if self.fps: time.sleep(1/self.fps)

    def _whats_the_plan(self, grid, pos):
        visited = set()
        fringe = deque([(pos, -1j, tuple())])
        moves = (1j, 1, -1j, -1)
        while fringe:
            pos, dir, path = fringe.popleft()

            if pos in visited: continue
            visited.add(pos)

            if grid.get(pos, 0) == 0:
                return deque(path)

            for t in moves:
                xdr = dir * t
                xto = pos + xdr
                if grid.get(xto, 0) != Grid.WALL:
                    fringe.append((xto, xdr, path + (xto,)))

        self.exploring = False


def fill_oxygen(grid):
    o = next(k for k, c in grid.items() if c == Grid.TANK)
    fringe = [o]
    visited = {o}
    steps = 0
    moves = (-1j, -1, 1j, 1)
    while fringe:
        tofill = set()
        for cur in fringe:
            for t in moves:
                xto = cur + t
                if xto in visited: continue
                visited.add(xto)
                if grid.get(xto) == Grid.SPACE:
                    tofill.add(xto)
        fringe = tofill
        if fringe:
            steps += 1
    return steps


def test():
    paiv.test_subject(fill_oxygen)

    s = """
 ##
#..##
#.#..#
#.O.#
 ###
""".strip('\n')
    symb = dict(zip(' .#O', [0, Grid.SPACE, Grid.WALL, Grid.TANK]))
    grid = dict((x + 1j*y, symb[c]) for y, row in enumerate(s.splitlines()) for x, c in enumerate(row))

    paiv.test(grid) == 4


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
