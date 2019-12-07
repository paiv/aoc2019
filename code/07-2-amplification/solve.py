#!/usr/bin/env python
import itertools
import paivlib as paiv
from collections import deque


def solve(text):
    mem = paiv.parse_ints_flatten(text)

    best = 0
    for phase in itertools.permutations(range(5, 10)):
        amps = [[list(mem), 0] for _ in phase]
        inputs = [deque([q]) for q in phase]
        inputs[0].append(0)

        i = 0
        while True:
            x = emu(i, amps[i], inputs[i], inputs[(i+1)%5])
            if x is None and i == 4:
                break
            i = (i + 1) % len(amps)

        sig = inputs[0][0]

        if sig > best:
            best = sig
            paiv.trace(best, phase)

    return best


def emu(id, image, input, output):
    mem, ip = image
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
            x = input.popleft()
            a = mem[ip + 1]
            mem[a] = x
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = a if ma else mem[a]
            output.append(x)
            ip += 2
            image[1] = ip
            return output[-1]

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

    image[1] = ip


def test():
    paiv.test_subject(solve)
    paiv.test('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5') == 139629729
    paiv.test('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10') == 18216


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
