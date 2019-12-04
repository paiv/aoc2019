#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text):
    a,b = map(int, text.split('-'))
    return sum(map(valid, range(a, b + 1)))


def valid(n):
    t = 10
    pair = False
    for x in digits(n):
        if x > t: return False
        if x == t: pair = True
        t = x
    return pair


def digits(n):
    while n:
        n, t = divmod(n, 10)
        yield t


def test():
    paiv.test_subject(valid)
    paiv.test(111111) == True
    paiv.test(223450) == False
    paiv.test(123789) == False

    paiv.test_subject(solve)
    paiv.test('111111-111113') == 3


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
