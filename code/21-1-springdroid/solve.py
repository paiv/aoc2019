#!/usr/bin/env python
import intcode as ic
import paivlib as paiv
from collections import deque


def solve(text):
    image = ic.IntcodeImage.loads(text)
    vm = ic.IntcodeVM(image)

    driver = Driver()
    vm.run(driver)


class Driver:
    def __init__(self):
        self.state = 0
        self.data = ''
        self.output = None

    def is_active(self):
        return True

    def read(self):
        if not self.output:
            spring = """
NOT C J
AND D J
NOT A T
OR T J
WALK
""".lstrip()
            self.output = deque(spring)
        s = self.output.popleft()
        return ord(s)

    def write(self, value):
        if 9 <= value < 128:
            print(chr(value), end='')
        else:
            print(value)


if __name__ == '__main__':
    print(solve(paiv.read_files()))
