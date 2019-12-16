#!/usr/bin/env python
import itertools as it
import paivlib as paiv


def solve(text, steps=100):
    xs = [*map(int, text.strip())]
    paiv.trace(xs)

    n = len(xs)
    pattern = [0, 1, 0, -1]

    def pat(n):
        a = it.cycle(pattern)
        b = it.chain.from_iterable([x] * n for x in a)
        return it.islice(b, 1, None)

    for _ in range(steps):
        xs = [abs(sum(x * p for x, p in zip(xs, pat(i)))) % 10 for i in range(1, n+1)]

    return ''.join(map(str, xs[:8]))


def test():
    paiv.test_subject(solve)
    paiv.test('12345678', 1) == '48226158'
    paiv.test('12345678', 2) == '34040438'
    paiv.test('12345678', 3) == '03415518'
    paiv.test('12345678', 4) == '01029498'
    paiv.test('80871224585914546619083218645595') == '24176176'
    paiv.test('19617804207202209144916044189917') == '73745418'
    paiv.test('69317163492948606335995924319873') == '52432133'


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
