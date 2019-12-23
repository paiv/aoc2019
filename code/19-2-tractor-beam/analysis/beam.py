#!/usr/bin/env python
import io
import sys


def beam(x, y):
    b = -1 if (x * x * 83 - y - y * y * 34) < 0 else 0
    if x < y:
        a = 1 if (x * y * y - x * y * (y - 12)) >= (x * x * 83 - y * y * 34) else 0
    else:
        a = 1 if (x * x * y - x * y * (x - 12)) >= (x * x * 83 - y * y * 34) else 0
    return a + b

so = io.StringIO()
for y in range(50):
    for x in range(50):
        c = '#' if beam(x, y) else '.'
        print(c, end='', file=so)
    print('', file=so)
print(so.getvalue())
