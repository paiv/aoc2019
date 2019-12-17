#!/usr/bin/env python
import intcode as ic
import paivlib as paiv


def solve(text):
    image = ic.IntcodeImage.loads(text)
    vm = ic.IntcodeVM(image)

    driver = Driver()
    vm.run(driver)

    paiv.trace(driver.data)
    s = driver.data
    bot = set('^v<>')
    grid = dict((x + 1j * y, '#' if c in bot else c)
        for y, row in enumerate(s.splitlines()) for x, c in enumerate(row))

    moves = (-1j, -1, 1j, 1)
    ans = sum(int(p.real * p.imag) for p, c in grid.items() if c == '#'
        if all(grid.get(p + t) == '#' for t in moves))
    return ans


class Driver:
    def __init__(self):
        self.data = ''

    def is_active(self):
        return True

    def read(self):
        raise Exception()

    def write(self, value):
        self.data += chr(value)


if __name__ == '__main__':
    print(solve(paiv.read_files()))
