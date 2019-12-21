#!/usr/bin/env python
import itertools


def terrain():
    ukn = [*itertools.product((False, True), repeat=3)]

    def inner(x, path):
        if x > 9:
            yield path[:10]
            return

        yield from inner(x + 1, path + (True,))

        # if x == 0: path = (2,)
        for v in ukn:
            yield from inner(x + 4, path + v + (True,))

    yield from inner(0, (True,))


def main():
    for i, sample in enumerate(sorted(set(terrain()), reverse=True)):
        s = ''.join('.#^'[i] for i in sample + (True,)*7)
        print(f'<option value="{s}">{i:>03} {s}</option>')


if __name__ == '__main__':
    main()
