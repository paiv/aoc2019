#!/usr/bin/env python
import paivlib as paiv


def solve(text, w=25, h=6):
    text = text.strip()
    n = w * h
    layers = [text[i:i+n] for i in range(0, len(text), n)]
    stats = [(s.count('0'), s.count('1') * s.count('2')) for s in layers]

    zmin = min(x for x,_ in stats)
    ans, = [y for i,(x,y) in enumerate(stats) if x == zmin]
    return ans


if __name__ == '__main__':
    print(solve(paiv.read_files()))
