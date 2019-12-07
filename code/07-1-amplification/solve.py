#!/usr/bin/env python -OO
import itertools
import paivlib as paiv


def solve(text):
    mem = paiv.parse_ints_flatten(text)

    best = 0
    for phase in itertools.permutations(range(5)):
        sig = 0
        for q in phase:
            sig = emu(list(mem), [q, sig])

        if sig > best:
            best = sig
            paiv.trace(best, phase)

    return best


def emu(mem, input):
    input = iter(input)
    ip = 0
    while ip < len(mem):
        op = mem[ip]
        ma = op // 100 % 10
        mb = op // 1000 % 10
        op %= 100

        if op == 1:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            mem[c] = x + y
            ip += 4

        elif op == 2:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            mem[c] = x * y
            ip += 4

        elif op == 3:
            x = next(input)
            a = mem[ip + 1]
            mem[a] = x
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = a if ma else mem[a]
            ip += 2
            return x

        elif op == 5:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            ip = y if (x != 0) else (ip + 3)

        elif op == 6:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            ip = y if (x == 0) else (ip + 3)

        elif op == 7:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            mem[c] = 1 if (x < y) else 0
            ip += 4

        elif op == 8:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = a if ma else mem[a]
            y = b if mb else mem[b]
            mem[c] = 1 if (x == y) else 0
            ip += 4

        elif op == 99:
            ip += 1
            break

        else:
            raise Exception(f'op {op}')


def test():
    paiv.test_subject(solve)
    paiv.test('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0') == 43210
    paiv.test('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0') == 54321
    paiv.test('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0') == 65210


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
