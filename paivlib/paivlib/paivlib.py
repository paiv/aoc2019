import sys
import re


VERBOSE = 2 if __debug__ else 1


def verbose(n):
    global VERBOSE
    VERBOSE = n


def trace(*args, **kwargs):
    if VERBOSE > 1: print(*args, file=sys.stderr, **kwargs)


def read_files(mode='r'):
    fn = sys.argv[1]
    with open(fn, mode=mode) as fp:
        return fp.read()


def parse_ints(s, dtype=int):
    rx = re.compile(r'-?\d+')
    return [[*map(dtype, n)] for n in map(rx.findall, s.splitlines())]


def parse_ints_flatten(s, dtype=int):
    xs = parse_ints(s, dtype=dtype)
    return [x for n in xs for x in n]


def l1_distance(a, b):
    if isinstance(a, complex):
        return abs(b.real - a.real) + abs(b.imag - a.imag)
    elif isinstance(a, tuple):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    raise Exception(f'{type(a)} {type(b)}')

l1_dist = l1_distance
manhattan_distance = l1_distance
