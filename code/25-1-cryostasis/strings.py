#!/usr/bin/env python
import string
import sys


def main(fn):
    with open(fn) as fp:
        mem = dict(enumerate(map(int, fp.read().split(','))))

    abc = string.ascii_letters + string.digits + ' \n!-\':,".?'
    valid = set(map(ord, abc))
    # valid = (set(range(32, 128)) | {10}) - {ord('\\')}

    def decode(o, n):
        def inner():
            for i in range(n):
                x = mem.get(o+i,0) + i + n
                if x not in valid: return
                yield x
        xs = list(inner())
        if len(xs) == n:
            return ''.join(map(chr, xs))


    off = 0
    while off < len(mem):
        for n in range(5, 2000):
            s = decode(off, n)
            if s:
                print(off, n)
                print(repr(s))
        off += 1



if __name__ == '__main__':
    main(*sys.argv[1:])
