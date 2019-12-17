#!/usr/bin/env python
import sys
import re


def main(fn):
    with open(fn) as fp:
        data = fp.read()
    data = [*map(int, re.findall(r'\-?\d+', data))]

    for y in range(41):
        for x in range(41):
            space = None
            if x == 0 or x == 40 or y == 0 or y == 40:
                space = False
            elif (x % 2) and (y % 2):
                space = True
            elif (x % 2 == 0) and (y % 2 == 0):
                space = False
            else:
                i = 252 + ((y // 2) + (y % 2) - 1) * 39 + x - 1
                q = data[i]
                space = q < 74
            c = '.' if space else '#'
            print(c, end='')
        print()


if __name__ == '__main__':
    main(*sys.argv[1:])
