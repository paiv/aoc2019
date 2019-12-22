#!/usr/bin/env python
import itertools
import paivlib as paiv


def solve(text, n=10007, query=2019):
    deck = shuffle(text, n)
    return deck.index(query)


def shuffle(text, n):
    deck = [*range(n)]

    for op in text.strip().splitlines():
        arg = op.split()[-1]

        if op.startswith('deal with'):
            v = int(arg)
            xs = list(deck)
            for x, i in zip(deck, itertools.count(0, v)):
                xs[i%n] = x
            deck = xs

        elif op.startswith('deal into'):
            deck = deck[::-1]

        elif op.startswith('cut'):
            v = int(arg)
            deck = deck[v:] + deck[:v]

    return deck


def test():
    paiv.test_subject(shuffle)

    s = """
deal with increment 7
deal into new stack
deal into new stack
"""
    paiv.test(s, 10) == [0,3,6,9,2,5,8,1,4,7]

    s = """
cut 6
deal with increment 7
deal into new stack
"""
    paiv.test(s, 10) == [3,0,7,4,1,8,5,2,9,6]

    s = """
deal with increment 7
deal with increment 9
cut -2
"""
    paiv.test(s, 10) == [6,3,0,7,4,1,8,5,2,9]

    s = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
    paiv.test(s, 10) == [9,2,5,8,1,4,7,0,3,6]

    paiv.test_subject(solve)

    paiv.test(s, 10, 8) == 3


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
