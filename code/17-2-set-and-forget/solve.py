#!/usr/bin/env python
import itertools
import operator
import paivlib as paiv
import sys
from collections import defaultdict, deque
from functools import reduce


def solve(text):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))

    mem[0] = 2

    driver = Driver()
    emu(mem, driver)

    return driver.dust


class Driver:
    def __init__(self):
        self.state = 0
        self.data = ''
        self.output = None

    def is_active(self):
        return True

    def read(self):
        s = self.output.popleft()
        return ord(s)

    def write(self, value):
        if self.state == 0:
            self.data += chr(value)
            if self.data.endswith('\n\n'):
                paiv.trace(self.data)
                self.state = 1
                self._trace_path()
        elif self.state == 1:
            if 0 < value < 128:
                paiv.trace(chr(value), end='')
            else:
                paiv.trace(repr(value))
                self.dust = value

    def _trace_path(self):
        bot = set('^v<>')
        grid = dict((x + 1j * y, '#' if c in bot else c)
            for y, row in enumerate(self.data.splitlines())
            for x, c in enumerate(row)
            if c != '.')
        pos, dir = next((x + 1j * y, c)
            for y, row in enumerate(self.data.splitlines())
            for x, c in enumerate(row)
            if c in bot)

        dir = dict(zip('^v<>', (-1j,1j,-1,1)))[dir]
        path = [pos]
        actions = list()
        while True:
            if grid.get(pos + dir):
                pos += dir
                actions.append(1)
                path.append(pos)
            elif grid.get(pos + dir * 1j):
                dir *= 1j
                actions.append('R')
            elif grid.get(pos + dir * -1j):
                dir *= -1j
                actions.append('L')
            else:
                break

        paiv.trace(actions)
        actions = [reduce(operator.add, g) for _, g in itertools.groupby(actions, key=lambda x: isinstance(x, int))]
        paiv.trace(actions)

        cmd = """A,B,A,C,B,A,C,B,A,C
L,12,L,12,L,6,L,6
R,8,R,4,L,12
L,12,L,6,R,12,R,8
n
"""
        self.output = deque(cmd)


def emu(mem, driver):
    ip = 0
    base = 0

    def param(a, ma):
        return mem[base + a] if (ma == 2) else (mem[a] if ma == 0 else a)
    def write(c, mc, x):
        if mc == 2: c += base
        mem[c] = x

    while driver.is_active():
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
            x = driver.read()
            a = mem[ip + 1]
            write(a, ma, x)
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = param(a, ma)
            ip += 2
            driver.write(x)

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
