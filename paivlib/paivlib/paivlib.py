import fileinput
import itertools
import operator
import sys
import re
from functools import reduce


VERBOSE = 2 if __debug__ else 1


def verbose(n):
    global VERBOSE
    VERBOSE = n


def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def read_files(mode='r'):
    with fileinput.input(mode=mode) as fp:
        return reduce(operator.add, fp)


def parse_ints(s, dtype=int):
    rx = re.compile(r'-?\d+')
    return [[*map(dtype, n)] for n in map(rx.findall, s.splitlines())]


def parse_ints_flatten(s, dtype=int):
    xs = parse_ints(s, dtype=dtype)
    return [x for n in xs for x in n]


class Ocr:
    tables = [
"""
A    B    C    E    F    G    H    I    J    K    L    P    R    U    Y     Z
.##..###...##..####.####..##..#..#..###...##.#..#.#....###..###..#..#.#...#.####.
#..#.#..#.#..#.#....#....#..#.#..#...#.....#.#.#..#....#..#.#..#.#..#.#...#....#.
#..#.###..#....###..###..#....####...#.....#.##...#....#..#.#..#.#..#..#.#....#..
####.#..#.#....#....#....#.##.#..#...#.....#.#.#..#....###..###..#..#...#....#...
#..#.#..#.#..#.#....#....#..#.#..#...#..#..#.#.#..#....#....#.#..#..#...#...#....
#..#.###...##..####.#.....###.#..#..###..##..#..#.####.#....#..#..##....#...####.
""",
"""
A       B       C       E       F       G       H       J       K       L       N       P       R       X       Z
..##....#####....####...######..######...####...#....#.....###..#....#..#.......#....#..#####...#####...#....#..######..
.#..#...#....#..#....#..#.......#.......#....#..#....#......#...#...#...#.......##...#..#....#..#....#..#....#.......#..
#....#..#....#..#.......#.......#.......#.......#....#......#...#..#....#.......##...#..#....#..#....#...#..#........#..
#....#..#....#..#.......#.......#.......#.......#....#......#...#.#.....#.......#.#..#..#....#..#....#...#..#.......#...
#....#..#####...#.......#####...#####...#.......######......#...##......#.......#.#..#..#####...#####.....##.......#....
######..#....#..#.......#.......#.......#..###..#....#......#...##......#.......#..#.#..#.......#..#......##......#.....
#....#..#....#..#.......#.......#.......#....#..#....#......#...#.#.....#.......#..#.#..#.......#...#....#..#....#......
#....#..#....#..#.......#.......#.......#....#..#....#..#...#...#..#....#.......#...##..#.......#...#....#..#...#.......
#....#..#....#..#....#..#.......#.......#...##..#....#..#...#...#...#...#.......#...##..#.......#....#..#....#..#.......
#....#..#####....####...######..#........###.#..#....#...###....#....#..######..#....#..#.......#....#..#....#..######..
""",
]

    class _Ocr1:
        def __init__(self, charmap):
            head, *_ = charmap.strip('\n').splitlines()
            abc = head.split()
            table = [*self._split(charmap)]
            height = len(table[-1])
            self.table = {abc[i]:char for i, char in enumerate(table)}
            self.rtable = {char:abc[i] for i, char in enumerate(table)}
            self.height = height

        def _split(self, text):
            lines = Ocr._bitmap(text)
            for k, g in itertools.groupby(zip(*lines), any):
                if k: yield tuple(zip(*g))

        def __getitem__(self, key):
            return self.rtable.get(key)

    def __init__(self):
        self.tables = [*map(Ocr._Ocr1, Ocr.tables)]

    def scan(self, text):
        def inner():
            bmap = [*zip(*Ocr._bitmap(text))]
            l = 0
            for r in range(1, len(bmap) + 1):
                if not any(x for s in bmap[l:r] for x in s):
                    if l + 1 != r:
                        yield '?'
                    l = r
                else:
                    x = tuple(zip(*bmap[l:r]))
                    for t in self.tables:
                        q = t[x]
                        if q is not None:
                            l = r
                            yield q
                            break
        return ''.join(inner())

    def _bitmap(text):
        t = re.sub(r'[^#.\n]', ' ', text).strip()
        return [[x == '#' for x in row] for row in t.splitlines()]

    def print(self, text, char_space=2):
        xs = (self.table[x] for x in text if x in self.table)
        sp = tuple((False,)*char_space for _ in range(self.height))
        xs = (x for p in xs for x in [p, sp])
        return Ocr._render([reduce(operator.add, row) for row in zip(*xs)])

    def _render(char):
        return '\n'.join(''.join('#' if x else '.' for x in row) for row in char)
