#!/usr/bin/env python -OO
import paivlib as paiv


def solve(s):
    t = paiv.parse_ints(s)
    paiv.trace(t)
    return sum(map(sum, t))


def test():
    paiv.test_subject(solve)
    paiv.test('3 2 1') == 6


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
