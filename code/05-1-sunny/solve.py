#!/usr/bin/env python
import paivlib as paiv


def solve(text):
    mem = paiv.parse_ints_flatten(text)
    emu(mem)


def emu(mem):
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
            x = int(input())
            a = mem[ip + 1]
            mem[a] = x
            ip += 2

        elif op == 4:
            a = mem[ip + 1]
            x = a if ma else mem[a]
            print(x)
            ip += 2

        elif op == 99:
            ip += 1
            break

        else:
            raise Exception(f'op {op}')

    return mem


def test():
    paiv.test_subject(emu)
    paiv.test([1,0,0,0,99]) == [2,0,0,0,99]
    paiv.test([2,3,0,3,99]) == [2,3,0,6,99]
    paiv.test([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    paiv.test([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
    paiv.test([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    paiv.test([1002,4,3,4,33]) == [1002,4,3,4,99]


if __name__ == '__main__':
    test()
    solve(paiv.read_files())
