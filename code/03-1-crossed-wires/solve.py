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

    wire1 = set(trace(wires[0]))
    wire2 = set(trace(wires[1]))
    xs = wire1 & wire2
    ans = min(paiv.l1_dist(start, p) for p in xs)
    return int(ans)


def test():
    paiv.test_subject(solve)
    paiv.test('R8,U5,L5,D3\nU7,R6,D4,L4\n') == 6
    paiv.test('''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83''') == 159
    paiv.test('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7''') == 135


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
