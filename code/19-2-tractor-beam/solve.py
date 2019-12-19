#!/usr/bin/env python
import intcode as ic
import paivlib as paiv
from collections import deque


def solve(text):
    image = ic.IntcodeImage.loads(text)

    def beam(x, y):
        driver = Driver([x, y])
        vm = ic.IntcodeVM(image)
        vm.run(driver)
        z, = driver.input
        return z

    x, y = 0, 0
    while True:
        while not beam(x, y + 99):
            x += 1
        if beam(x + 99, y):
            return x * 10000 + y
        y += 1


class Driver:
    def __init__(self, output):
        self.output = deque(output)
        self.input = list()

    def is_active(self):
        return not self.input

    def read(self):
        return self.output.popleft()

    def write(self, value):
        self.input.append(value)


if __name__ == '__main__':
    print(solve(paiv.read_files()))
