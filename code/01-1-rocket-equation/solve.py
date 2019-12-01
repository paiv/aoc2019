#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text):
    xs = paiv.parse_ints_flatten(text)
    def req(x): return x // 3 - 2
    return sum(map(req, xs))


def test():
    paiv.test_subject(solve)
    paiv.test('12') == 2
    paiv.test('14') == 2
    paiv.test('1969') == 654
    paiv.test('100756') == 33583


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
