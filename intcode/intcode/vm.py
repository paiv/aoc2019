import io


class IntcodeImage:
    def __init__(self, program, ip=0):
        if isinstance(program, list):
            program = dict(enumerate(program))
        self.program = program
        self.ip = ip

    def __copy__(self):
        return IntcodeImage(type(self.program)(self.program), ip=self.ip)

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
    def __init__(self, image):
        self.image = image

    def run(self, driver=None):
        if driver is None:
            driver = IntcodeDriver()

        image = self.image.copy()
        image.ip = self._emu(image.program, image.ip, driver)
        self.image = image

    def _emu(self, mem, ip, driver):
        base = 0

        def param(a, ma, default=0):
            return mem.get(base + a, default) if (ma == 2) else (mem.get(a, default) if ma == 0 else a)
        def write(c, mc, x):
            if mc == 2: c += base
            mem[c] = x

        while driver.is_active():
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
                raise Exception(f'op {op}')

        return ip
