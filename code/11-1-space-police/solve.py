#!/usr/bin/env python -OO
import io
import paivlib as paiv
import time
from collections import defaultdict, deque


def solve(text):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))

    robot = Robot(trace=False)
    emu(mem, robot)

    return len(robot.grid)


class Robot:
    def __init__(self, trace=False):
        self.trace = trace
        self.pos = 0j
        self.dir = -1j
        self.grid = defaultdict(int)
        self.state = 0

    def __str__(self):
        grid = dict(self.grid)
        grid[self.pos] = grid.get(self.pos, 0)
        so = io.StringIO()
        xs = [int(p.real) for p in grid] or [0]
        ys = [int(p.imag) for p in grid] or [0]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                p = x + 1j * y
                if p == self.pos:
                    q = self.dir
                    c = '>' if q.real == 1 else ('<' if q.real == -1 else ('^' if q.imag == -1 else 'v'))
                else:
                    c = '#' if grid.get(p) else '.'
                so.write(c)
            so.write('\n')
        return so.getvalue()

    def read(self):
        color = self.grid[self.pos]
        return color

    def write(self, value):
        if self.state == 0:
            self.grid[self.pos] = value
            self.state = 1
        elif self.state == 1:
            self.dir *= 1j if value else -1j
            self.pos += self.dir
            self.state = 0
            if self.trace:
                print(self)
                time.sleep(0.5)

    def is_running(self):
        return True


def emu(mem, robot):
    ip = 0
    base = 0

    def param(a, ma):
        return mem[base + a] if (ma == 2) else (mem[a] if ma == 0 else a)
    def write(c, mc, x):
        if mc == 2: c += base
        mem[c] = x

    while robot.is_running():
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
            x = robot.read()
            a = mem[ip + 1]
            write(a, ma, x)
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = param(a, ma)
            robot.write(x)
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
