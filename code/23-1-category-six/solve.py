#!/usr/bin/env python -OO
import intcode as ic
import paivlib as paiv
from collections import defaultdict, deque


def solve(text):
    image = ic.IntcodeImage.loads(text)

    mbus = defaultdict(deque)
    machines = [Machine(image, mbus, name=i) for i in range(50)]

    while True:
        for proc in machines:
            if proc.is_running():
                proc.step()

            if mbus[255]:
                return mbus[255][0][2]


class Machine:
    def __init__(self, image, mbus, name=0):
        self.name = name
        self.driver = Driver(name, mbus)
        self.vm = ic.IntcodeVM(image.copy(), driver=self.driver)

    def is_running(self):
        return self.driver.is_active()

    def step(self):
        return self.vm.limited_run()


class Driver:
    def __init__(self, name, mbus):
        self.name = name
        self.mbus = mbus
        self.rstate = 0
        self.rpacket = None
        self.wstate = 0
        self.waddr = None
        self.wpacket = None

    def is_active(self):
        return True

    @property
    def read_queue(self):
        return self.mbus[self.name]

    def read(self):
        if self.rstate == 0:
            self.rstate = 1
            return self.name
        elif self.rstate == 1 and not self.read_queue:
            return -1
        elif self.rstate == 1:
            self.rpacket = self.read_queue.popleft()
            self.rstate = 2
            return self.rpacket[1]
        elif self.rstate == 2:
            addr, packet = self.rpacket[0], self.rpacket[1:]
            paiv.trace(f'{self.name:02} <- {addr:02}  {packet}')
            x, self.rpacket = packet[1], None
            self.rstate = 1
            return x

    def write(self, value):
        if self.wstate == 0:
            self.waddr = value
            self.wpacket = [self.name]
            self.wstate = 1
        elif self.wstate == 1:
            self.wpacket.append(value)
            self.wstate = 2
        elif self.wstate == 2:
            p, self.wpacket = self.wpacket, None
            packet = tuple((*p, value))
            paiv.trace(f'{self.name:02} -> {self.waddr:02}  {packet[1:]}')
            self.mbus[self.waddr].append(packet)
            self.wstate = 0


if __name__ == '__main__':
    print(solve(paiv.read_files()))
