#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text):
    xs = paiv.parse_ints_flatten(text)
    def req1(x): return x // 3 - 2
    def req(n):
        r = 0
        while True:
            n = req1(n)
            if n <= 0: return r
            r += n
    return sum(map(req, xs))


def test():
    paiv.test_subject(solve)
    paiv.test('12') == 2
    paiv.test('14') == 2
    paiv.test('1969') == 966
    paiv.test('100756') == 50346


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
