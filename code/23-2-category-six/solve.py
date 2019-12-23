#!/usr/bin/env python -OO
import intcode as ic
import paivlib as paiv
from collections import defaultdict, deque


_ticks = [0]


def solve(text):
    image = ic.IntcodeImage.loads(text)

    mbus = defaultdict(deque)
    machines = [Machine(image, mbus, name=i) for i in range(50)]

    nat = None
    seen = None
    _ticks[0] = 0

    while True:
        for proc in machines:
            if proc.is_running():
                _ticks[0] += proc.step()

            if mbus[255]:
                nat = mbus[255].popleft()

        if not nat or any(mbus.values()) or any(not proc.is_idle for proc in machines):
            continue

        paiv.trace(f'{_ticks[0]:06x}: 00 <- nat  {nat}')
        if nat[2] == seen:
            return seen
        seen = nat[2]
        mbus[0].append(nat)


class Machine:
    def __init__(self, image, mbus, name=0):
        self.name = name
        self.driver = Driver(name, mbus)
        self.vm = ic.IntcodeVM(image.copy(), driver=self.driver)

    def is_running(self):
        return self.driver.is_active()

    @property
    def is_idle(self):
        return self.driver.idle

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
        self.idle = False

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
            self.idle = True
            return -1
        elif self.rstate == 1:
            self.idle = False
            self.rpacket = self.read_queue.popleft()
            self.rstate = 2
            return self.rpacket[1]
        elif self.rstate == 2:
            addr, packet = self.rpacket[0], self.rpacket[1:]
            paiv.trace(f'{_ticks[0]:06x}: {self.name:02} <- {addr:02}  {packet}')
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
            paiv.trace(f'{_ticks[0]:06x}: {self.name:02} -> {self.waddr:02}  {packet[1:]}')
            self.mbus[self.waddr].append(packet)
            self.wstate = 0


if __name__ == '__main__':
    print(solve(paiv.read_files()))
