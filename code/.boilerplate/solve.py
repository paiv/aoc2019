#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text):
    xs = paiv.parse_ints(text)
    paiv.trace(xs)
    return sum(map(sum, xs))


def test():
    paiv.test_subject(solve)
    paiv.test('3 2 1') == 6


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
