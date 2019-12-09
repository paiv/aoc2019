#!/usr/bin/env python -OO
import paivlib as paiv
from collections import defaultdict, deque


def solve(text, input=[1]):
    data = paiv.parse_ints_flatten(text)
    mem = defaultdict(int)
    mem.update((i,x) for i,x in enumerate(data))

    input = deque(input)
    output = deque()
    emu(mem, input=input, output=output)

    return list(output)


def emu(mem, input, output):
    ip = 0
    base = 0

    def param(a, ma):
        return mem[base + a] if (ma == 2) else (mem[a] if ma == 0 else a)
    def write(c, mc, x):
        if mc == 2: c += base
        mem[c] = x

    while True:
        op = mem[ip]
        ma = op // 100 % 10
        mb = op // 1000 % 10
        mc = op // 10000 % 10
        op %= 100

        if op == 1:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, x + y)
            ip += 4

        elif op == 2:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, x * y)
            ip += 4

        elif op == 3:
            x = int(input.popleft())
            a = mem[ip + 1]
            write(a, ma, x)
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = param(a, ma)
            output.append(x)
            ip += 2

        elif op == 5:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = param(a, ma)
            y = param(b, mb)
            ip = y if (x != 0) else (ip + 3)

        elif op == 6:
            a = mem[ip + 1]
            b = mem[ip + 2]
            x = param(a, ma)
            y = param(b, mb)
            ip = y if (x == 0) else (ip + 3)

        elif op == 7:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, 1 if (x < y) else 0)
            ip += 4

        elif op == 8:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = param(a, ma)
            y = param(b, mb)
            write(c, mc, 1 if (x == y) else 0)
            ip += 4

        elif op == 9:
            a = mem[ip + 1]
            x = param(a, ma)
            base += x
            ip += 2

        elif op == 99:
            ip += 1
            break

        else:
            raise Exception(f'op {op}')


def test():
    paiv.test_subject(solve)
    paiv.test('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99') == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    paiv.test('1102,34915192,34915192,7,4,7,99,0') == [1219070632396864]
    paiv.test('104,1125899906842624,99') == [1125899906842624]


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
