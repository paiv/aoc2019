import io


class IntcodeImage:
    def __init__(self, program, ip=0, base=0):
        if isinstance(program, list):
            program = dict(enumerate(program))
        self.program = program
        self.ip = ip
        self.base = base

    def __copy__(self):
        return IntcodeImage(type(self.program)(self.program), ip=self.ip, base=self.base)

    def copy(self):
        return self.__copy__()

    def load(fp):
        data = list()
        state = 0
        s = ''
        while True:
            x = fp.read(1)
            if not x: break
            if x.isdigit():
                s += x
            elif not s and x == '-':
                s += x
            elif s:
                data.append(int(s))
                s = ''
        if s:
            data.append(int(s))

        image = IntcodeImage(data, ip=0)
        return image

    def loads(s):
        with io.StringIO(s) as fp:
            return IntcodeImage.load(fp)

    def patch(self, diff):
        self.program.update(diff)


class IntcodeDriver:
    def is_active(self):
        return True

    def read(self):
        raise Exception()

    def write(self, value):
        pass


class IntcodeVM:
    def __init__(self, image, driver=None):
        self.image = image
        self.driver = driver

    def run(self, driver=None):
        self.limited_run(driver=driver, max_time=None)

    def limited_run(self, driver=None, max_time=1):
        if driver is None:
            driver = self.driver or IntcodeDriver()

        time_used = self._emu(self.image, driver, time_limit=max_time)
        return time_used

    def _emu(self, image, driver, time_limit=None):
        mem = image.program
        ip = image.ip

        time_used = 0

        def param(a, ma, default=0):
            return mem.get(image.base + a, default) if (ma == 2) else (mem.get(a, default) if ma == 0 else a)

        def write(c, mc, x):
            if mc == 2: c += image.base
            mem[c] = x

        while driver.is_active() and (time_limit is None or time_used < time_limit):
            time_used += 1

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
                x = driver.read()
                a = mem[ip + 1]
                write(a, ma, x)
                ip += 2

            elif op == 4:
                a = mem[ip + 1]
                x = param(a, ma)
                ip += 2
                driver.write(x)

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
                image.base += x
                ip += 2

            elif op == 99:
                ip += 1
                break

            else:
                raise Exception(f'opcode {op}')

        image.ip = ip
        return time_limit


class IntcodeDebugVM:
    def __init__(self, image=None, driver=None):
        self.image = image
        self.driver = driver
        self.running = False
        self.debugger = None
        self.step_break = False
        self.stop_at_entry = True
        self.changed_memory = dict()
        self.breakpoints = dict()
        self.ip_breaks = set()

    def run(self, driver=None):
        if driver is not None:
            self.driver = driver
        elif self.driver is None:
            self.driver = IntcodeDriver()

        image = self.image
        self.running = True
        (image.ip, image.base) = self._emu(image.program, image.ip, image.base, self.driver)

    def single_step(self):
        image = self.image
        self.step_break = True
        (image.ip, image.base) = self._emu(image.program, image.ip, image.base, self.driver)

    def add_ip_break(self, ip):
        spec = ('ip', ip)
        self._add_breakpoint(spec)
        self._rebuild_breakpoints()

    def update_breakpoints(self, breakpoints=None):
        if not breakpoints: return
        for spec in breakpoints.values():
            self._add_breakpoint(spec)
        self._rebuild_breakpoints()

    def _add_breakpoint(self, spec):
        if spec in self.breakpoints.values():
            return
        id = max(self.breakpoints, default=0) + 1
        self.breakpoints[id] = spec

    def _rebuild_breakpoints(self):
        bps = self.breakpoints
        ips = set(i for k, i in bps.values() if k == 'ip')
        self.ip_breaks = ips

    def _emu(self, mem, ip, base, driver):
        self.changed_memory = dict()

        def param(a, ma, default=0):
            return mem.get(base + a, default) if (ma == 2) else (mem.get(a, default) if ma == 0 else a)

        def write(c, mc, x):
            if mc == 2: c += base
            t, mem[c] = mem.get(c,0), x
            if self.debugger and x != t:
                self.changed_memory[c] = x

        ignore_ip_breaks_once = True

        while driver.is_active():
            if self.debugger:
                if self.stop_at_entry:
                    self.stop_at_entry = False
                    return (ip, base)
                if (not ignore_ip_breaks_once) and (ip in self.ip_breaks):
                    return (ip, base)
            ignore_ip_breaks_once = False

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
                x = driver.read()
                a = mem[ip + 1]
                write(a, ma, x)
                ip += 2

            elif op == 4:
                a = mem[ip + 1]
                x = param(a, ma)
                ip += 2
                driver.write(x)

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
                raise Exception(f'opcode {op}')

            if self.debugger and self.step_break:
                self.step_break = False
                return (ip, base)

        self.running = False
        return (ip, base)
