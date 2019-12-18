#!/usr/bin/env python
import intcode as ic
import itertools
import operator
import paivlib as paiv
from collections import deque
from functools import reduce


def solve(text):
    image = ic.IntcodeImage.loads(text)
    image.patch({0: 2})
    vm = ic.IntcodeVM(image)

    driver = Driver()
    vm.run(driver)

    return driver.dust


class Driver:
    def __init__(self):
        self.state = 0
        self.data = ''
        self.output = None

    def is_active(self):
        return True

    def read(self):
        s = self.output.popleft()
        return ord(s)

    def write(self, value):
        if self.state == 0:
            self.data += chr(value)
            if self.data.endswith('\n\n'):
                paiv.trace(self.data)
                self.state = 1

                moves = self._trace_path()
                cmd = self._program(moves)
                cmd += '\nn\n'
                self.output = deque(cmd)

        elif self.state == 1:
            if 0 < value < 128:
                paiv.trace(chr(value), end='')
            else:
                paiv.trace(repr(value))
                self.dust = value

    def _trace_path(self):
        bot = set('^v<>')
        grid = dict((x + 1j * y, '#' if c in bot else c)
            for y, row in enumerate(self.data.splitlines())
            for x, c in enumerate(row)
            if c != '.')
        pos, dir = next((x + 1j * y, c)
            for y, row in enumerate(self.data.splitlines())
            for x, c in enumerate(row)
            if c in bot)

        dir = dict(zip('^v<>', (-1j,1j,-1,1)))[dir]
        path = [pos]
        actions = list()
        while True:
            if grid.get(pos + dir):
                pos += dir
                actions.append(1)
                path.append(pos)
            elif grid.get(pos + dir * 1j):
                dir *= 1j
                actions.append('R')
            elif grid.get(pos + dir * -1j):
                dir *= -1j
                actions.append('L')
            else:
                break

        return actions

    def _program(self, actions):
        paiv.trace(','.join(map(str, actions)))
        actions = [reduce(operator.add, g) for _, g in itertools.groupby(actions, key=lambda x: isinstance(x, int))]
        paiv.trace(','.join(map(str, actions)))

        for a in range(4, 13, 2):
            A = actions[:a]
            for b in range(4, 13, 2):
                for c in range(4, 13, 2):
                    B = C = None
                    prog = [A]
                    i = a
                    while i < len(actions):
                        if actions[i:i+a] == A:
                            prog.append(A)
                            i += a
                        elif B is None:
                            B = actions[i:i+b]
                            prog.append(B)
                            i += b
                        elif actions[i:i+b] == B:
                            prog.append(B)
                            i += b
                        elif C is None:
                            C = actions[i:i+c]
                            prog.append(C)
                            i += c
                        elif actions[i:i+c] == C:
                            prog.append(C)
                            i += c
                        else:
                            break
                    else:
                        if B is None or C is None: continue
                        M = [('A' if x == A else 'B' if x == B else 'C') for x in prog]
                        cmd = [','.join(map(str, xs)) for xs in [M, A, B, C]]
                        paiv.trace(cmd)
                        if all(len(s) <= 20 for s in cmd):
                            return '\n'.join(cmd)


if __name__ == '__main__':
    print(solve(paiv.read_files()))
