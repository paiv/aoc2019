#!/usr/bin/env python
import paivlib as paiv
import sys
from collections import defaultdict


def solve(text):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))
    driver = Driver()
    emu(mem, driver)

    paiv.trace(driver.data)
    s = driver.data
    bot = set('^v<>')
    grid = dict((x + 1j * y, '#' if c in bot else c)
        for y, row in enumerate(s.splitlines()) for x, c in enumerate(row))

    moves = (-1j, -1, 1j, 1)
    ans = sum(int(p.real * p.imag) for p, c in grid.items() if c == '#'
        if all(grid.get(p + t) == '#' for t in moves))
    return ans


class Driver:
    def __init__(self):
        self.data = ''

    def is_active(self):
        return True

    def read(self):
        raise Exception()

    def write(self, value):
        self.data += chr(value)


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
