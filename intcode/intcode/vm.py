import copy


class IntcodeImage:
    def __init__(self, program, ip=0):
        self.program = program
        self.ip = ip

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


class IntcodeVM:
    def __init__(self, image):
        self.image = image

    def run(self):
        program = copy(self.image.program)
        ip = self.image.ip

        self.image = IntcodeImage(program, ip=ip)
        return program[0]
