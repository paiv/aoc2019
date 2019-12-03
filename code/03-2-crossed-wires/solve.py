#!/usr/bin/env python
import paivlib as paiv


def solve(text):
    wires = [line.split(',') for line in text.splitlines() if line]

    moves = {'R': 1, 'L': -1, 'U': 1j, 'D': -1j}
    start = 1+1j

    def trace(wire):
        pos = start
        for op in wire:
            m = op[0]
            n = int(op[1:])
            dir = moves[m]
            for _ in range(n):
                pos += dir
                yield pos

    wire1 = {p:n for n, p in enumerate(trace(wires[0]), 1)}
    wire2 = {p:n for n, p in enumerate(trace(wires[1]), 1)}
    xs = set(wire1) & set(wire2)
    ans = min(wire1[p] + wire2[p] for p in xs)
    return ans


def test():
    paiv.test_subject(solve)
    paiv.test('R8,U5,L5,D3\nU7,R6,D4,L4\n') == 30
    paiv.test('''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83''') == 610
    paiv.test('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7''') == 410


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
