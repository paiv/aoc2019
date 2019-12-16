#!/usr/bin/env python -OO
import paivlib as paiv


def solve(text, steps=100):
    xs = [*map(int, text.strip())]
    paiv.trace(xs)

    xs = xs * 10000
    off = int(text[:7])
    paiv.trace(off)

    # bottom submatrix is upper triangular due to pattern being
    # ... 0 0 0 0 0 1 1 1 1 1 ...

    for _ in range(steps):
        m = sum(xs[off:])
        for i, x in enumerate(xs[off:], off):
            m, xs[i] = m - xs[i], abs(m) % 10

    return ''.join(map(str, xs[off:off+8]))


def test():
    paiv.test_subject(solve)

    paiv.test('03036732577212944063491565474664') == '84462026'
    paiv.test('02935109699940807407585447034323') == '78725270'
    paiv.test('03081770884921959731165446850517') == '53553731'


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
