#!/usr/bin/env python
import paivlib as paiv


def solve(text, target=19690720):
    code = paiv.parse_ints_flatten(text)

    for noun in range(100):
        for verb in range(100):
            if prog(code, noun, verb) == target:
                return noun * 100 + verb


def prog(mem, noun=12, verb=2):
    mem = list(mem)
    mem[1] = noun
    mem[2] = verb
    emu(mem)
    return mem[0]


def emu(mem):
    ip = 0
    while ip < len(mem):
        op = mem[ip]
        if op == 1:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = mem[a]
            y = mem[b]
            mem[c] = x + y
            ip += 4
        elif op == 2:
            a = mem[ip + 1]
            b = mem[ip + 2]
            c = mem[ip + 3]
            x = mem[a]
            y = mem[b]
            mem[c] = x * y
            ip += 4
        elif op == 99:
            ip += 1
            break
        else:
            raise Exception(f'op {repr(op)}')
    return mem


def test():
    paiv.test_subject(emu)
    paiv.test([1,0,0,0,99]) == [2,0,0,0,99]
    paiv.test([2,3,0,3,99]) == [2,3,0,6,99]
    paiv.test([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    paiv.test([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
    paiv.test([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]

    paiv.test_subject(prog)
    paiv.test([1,0,0,0,99,0,0,0,0,0,0,0,7]) == 9
    paiv.test([2,0,0,0,99,0,0,0,0,0,0,0,7]) == 14
    paiv.test([99,0,0]) == 99


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
