#!/usr/bin/env python
import heapq
import intcode as ic
import io
import paivlib as paiv
import sys
import time
from collections import defaultdict, deque


def solve(text):
    image = ic.IntcodeImage.loads(text)
    vm = ic.IntcodeVM(image)

    droid = Droid(trace=True, fps=144)
    vm.run(droid)

    paiv.trace(str(droid).rstrip())

    ans = len(droid.find_path(0, droid.pos))
    return ans


class Grid:
    SPACE = 1
    WALL = 2
    BOT = 3
    TANK = 4


class Droid:
    def __init__(self, trace=False, fps=2):
        self.trace = trace
        self.fps = fps or 1
        self.grid = defaultdict(int)
        self.pos = 0
        self.plan = None
        self.grid[self.pos] = Grid.SPACE

    def __str__(self):
        grid = dict(self.grid)
        #        01234
        chars = ' .#DX'
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
        return self.grid[self.pos] != Grid.TANK

    moves = [1, 0, 2, 3, 0, 4]
    keyb = dict(zip('wasd', (-1j, -1, 1j, 1)))

    def read(self):
        if 0:
            t = None
            while not t:
                c = sys.stdin.read(1).rstrip()
                t = self.keyb.get(c)
            xto = self.pos + t
            self.plan = deque([xto])

        else:
            if not self.plan:
                self.plan = self._whats_the_plan(self.grid, self.pos)
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

    def find_path(self, sfrom, sto):
        visited = set()
        fringe = [(0, (sfrom.real, sfrom.imag), tuple())]
        moves = (-1j, -1, 1j, 1)
        grid = dict(self.grid)
        while fringe:
            _, (x, y), path = heapq.heappop(fringe)
            pos = x + 1j * y
            if pos == sto:
                return path
            if pos in visited: continue
            visited.add(pos)

            for t in moves:
                xto = pos + t
                x = grid.get(xto)
                if x == Grid.SPACE or x == Grid.TANK:
                    w = paiv.l1_dist(xto, sto)
                    p = (xto.real, xto.imag)
                    heapq.heappush(fringe, (len(path) + 1 + w, p, path + (p,)))

    def _whats_the_plan(self, grid, pos):
        visited = set()
        fringe = deque([(pos, tuple())])
        moves = (-1j, -1, 1j, 1)
        while fringe:
            pos, path = fringe.popleft()

            if pos in visited: continue
            visited.add(pos)

            if grid.get(pos, 0) == 0:
                return deque(path)

            for t in moves:
                xto = pos + t
                if grid.get(xto, 0) != Grid.WALL:
                    fringe.append((xto, path + (xto,)))


if __name__ == '__main__':
    print(solve(paiv.read_files()))
