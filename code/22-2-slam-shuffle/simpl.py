#!/usr/bin/env python
import sys
import z3


def main(fn):
    with open(fn) as fp:
        text = fp.read()

    M = 119315717514047
    driver = MyDriver(M, 2020)

    for s in text.strip().splitlines():
        *_, arg = s.split()

        if s.startswith('deal with'):
            driver.deal_with_increment(int(arg))
        elif s.startswith('deal into'):
            driver.deal_into_new_stack()
        elif s.startswith('cut'):
            driver.cut(int(arg))

    ans = driver.simplify()
    print(ans)


class MyDriver:
    def __init__(self, m, x):
        self.m = m
        self.x = x
        self.a = 1
        self.b = 0

    def simplify(self):
        return (self.a % self.m, self.b % self.m)

    def deal_with_increment(self, value):
        self.a = self.a * value % self.m
        self.b = self.b * value % self.m

    def deal_into_new_stack(self):
        self.a = -self.a % self.m
        self.b = -(self.b + 1) % self.m

    def cut(self, value):
        self.b = (self.b - value) % self.m


class Z3driver:
    def __init__(self, m, x):
        self.m = m
        self.x = x
        self.a = z3.Int('a')
        self.b = z3.Int('b')

    def simplify(self):
        return (z3.simplify(self.a % self.m), z3.simplify(self.b % self.m))

    def deal_with_increment(self, value):
        self.a = self.a * value
        self.b = self.b * value

    def deal_into_new_stack(self):
        self.a = -self.a
        self.b = -(self.b + 1)

    def cut(self, value):
        self.b = (self.b - value)


if __name__ == '__main__':
    main(*sys.argv[1:])
