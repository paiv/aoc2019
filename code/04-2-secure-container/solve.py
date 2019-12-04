#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text):
    a,b = map(int, text.split('-'))
    return sum(map(valid, range(a, b + 1)))


def valid(n):
    t = 10
    pair = 0
    valid = False
    for x in digits(n):
        if x > t: return False
        if x == t:
            pair += 1
        else:
            if pair == 2: valid = True
            pair = 1
        t = x
    return valid or pair == 2


def digits(n):
    while n:
        n, t = divmod(n, 10)
        yield t


def test():
    paiv.test_subject(valid)
    paiv.test(112233) == True
    paiv.test(123444) == False
    paiv.test(111122) == True

    paiv.test_subject(solve)
    paiv.test('111121-111123') == 1


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
