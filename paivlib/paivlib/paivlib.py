import fileinput
import operator
import sys
import re
from functools import reduce


VERBOSE = 2 if __debug__ else 1


def verbose(n):
    global VERBOSE
    VERBOSE = n


def print_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def trace(*args, **kwargs):
    if VERBOSE > 1: print_stderr(*args, **kwargs)


def read_files(mode='r'):
    with fileinput.input(mode=mode) as fp:
        return reduce(operator.add, fp)


def parse_ints(s, dtype=int):
    rx = re.compile(r'-?\d+')
    return [[*map(dtype, n)] for n in map(rx.findall, s.splitlines())]


def parse_ints_flatten(s, dtype=int):
    xs = parse_ints(s, dtype=dtype)
    return [x for n in xs for x in n]
