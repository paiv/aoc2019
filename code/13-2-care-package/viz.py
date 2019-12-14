#!/usr/bin/env python
import io
import paivlib as paiv
import time
from collections import defaultdict, deque


def solve(text):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))

    trace = deque()
    arcade = Arcade(trace=trace)
    mem[0] = 2
    yield from emu(mem, arcade, trace)


class Arcade:
    def __init__(self, trace=False, fps=None):
        self.trace = trace
        self.fps = fps
        self.grid = defaultdict(int)
        self.state = 0
        self.cur = 0
        self.score = None
        self.ball = None
        self.paddle = None

    def __str__(self):
        grid = dict(self.grid)
        chars = '.%#_*'
        so = io.StringIO()
        # so.write(f'score: {self.score}\n')
        xs = [int(p.real) for p in grid] or [0]
        ys = [int(p.imag) for p in grid] or [0]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                p = x + 1j * y
                c = chars[grid.get(p, 0)]
                so.write(c)
            so.write('\n')
        return so.getvalue().rstrip('\n')

    def read(self):
        a, b = self.paddle.real, self.ball.real
        return 1 if a < b else -1 if a > b else 0

    def write(self, value):
        if self.state == 0:
            self.cur = value
            self.state = 1
        elif self.state == 1:
            self.cur += 1j * value
            self.state = 2
        elif self.state == 2:
            if self.cur == -1:
                self.score = value
            else:
                self.grid[self.cur] = value
                if value == 3:
                    self.paddle = self.cur
                elif value == 4:
                    self.ball = self.cur
            self.state = 0
            if self.trace is not None and self.score is not None:
                self.trace.append(str(self))
                if self.fps:
                    time.sleep(1/self.fps)


def emu(mem, arcade, trace):
    ip = 0
    base = 0

    def param(a, ma):
        return mem[base + a] if (ma == 2) else (mem[a] if ma == 0 else a)
    def write(c, mc, x):
        if mc == 2: c += base
        mem[c] = x

    while True:
        op = mem[ip]
        ma = op // 100 % 10
        mb = op // 1000 % 10
        mc = op // 10000 % 10
        op %= 100

        if op == 1:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, x + y)
            ip += 4

        elif op == 2:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, x * y)
            ip += 4

        elif op == 3:
            x = arcade.read()
            a = mem[ip + 1]
            write(a, ma, x)
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = param(a, ma)
            arcade.write(x)
            ip += 2
            while trace:
                yield trace.popleft()

        elif op == 5:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = param(a, ma)
            y = param(b, mb)
            ip = y if (x != 0) else (ip + 3)

        elif op == 6:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = param(a, ma)
            y = param(b, mb)
            ip = y if (x == 0) else (ip + 3)

        elif op == 7:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, 1 if (x < y) else 0)
            ip += 4

        elif op == 8:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, 1 if (x == y) else 0)
            ip += 4

        elif op == 9:
            a = mem[ip + 1]
            x = param(a, ma)
            base += x
            ip += 2

        elif op == 99:
            ip += 1
            break

        else:
            raise Exception(f'op {op}')


def viz(file, output=None, rate=1, scale=1):
    text = file.read()

    with paiv.Sprites(cwd='sprites') as sprites:
        with paiv.VideoRenderer(output, rate=rate, scale=scale, sprites=sprites) as r:
            sprites.remap('.%#_*', 'bg wall block paddle ball'.split())
            frames = solve(text)
            r.render(frames)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Input file')
    parser.add_argument('-r', '--rate', default=20, type=float, help='Frame rate')
    parser.add_argument('-z', '--scale', default=1, type=int, help='Picture scale factor')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()

    viz(file=args.file, output=args.output, rate=args.rate, scale=args.scale)
