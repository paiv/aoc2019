#!/usr/bin/env python
import io
import paivlib as paiv
import time
from collections import defaultdict


def solve(text):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))

    arcade = Arcade(trace=False, fps=30)
    mem[0] = 2
    emu(mem, arcade)

    s = str(arcade).strip()
    paiv.trace(s)
    return arcade.score


class Arcade:
    def __init__(self, trace=False, fps=2):
        self.trace = trace
        self.fps = fps or 1
        self.grid = defaultdict(int)
        self.state = 0
        self.cur = 0
        self.score = None
        self.ball = None
        self.paddle = None

    def __str__(self):
        grid = dict(self.grid)
        chars = ' #█▂ⓧ'
        so = io.StringIO()
        xs = [int(p.real) for p in grid] or [0]
        ys = [int(p.imag) for p in grid] or [0]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                p = x + 1j * y
                c = chars[grid.get(p, 0)]
                so.write(c)
            so.write('\n')
        so.write(f'score: {self.score}\n')
        return so.getvalue()

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
            if self.trace and self.score is not None:
                print(self)
                time.sleep(1/self.fps)


def emu(mem, arcade):
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


if __name__ == '__main__':
    print(solve(paiv.read_files()))
