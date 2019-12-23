#!/usr/bin/env python -OO
import intcode as ic
import io
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

    grid = dict()
    offset = 0

    for y in range(50):
        for x in range(offset, 50):
            i = beam(x, y)
            grid[x, y] = i
            if not i and grid.get((x-1,y)):
                break
        offset = next((x for x in range(offset, 50) if grid[x,y]), offset)

    paiv.trace(dump(grid))

    return sum(grid.values())


def dump(grid):
    chars = '.#'
    so = io.StringIO()
    xs = [p[0] for p in grid] or [0]
    ys = [p[1] for p in grid] or [0]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            c = chars[grid.get((x,y), 0)]
            so.write(c)
        so.write('\n')
    return so.getvalue().rstrip('\n')


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
