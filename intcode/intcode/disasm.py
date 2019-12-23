import io
from .vm import IntcodeImage


class IntcodeDisasm:
    def __init__(self, output=None, analyze=False):
        self.output = output or io.StringIO()
        self.analyze = analyze
        self.ip = 0
        self.base = 0

    def process(self, program, ip=None, base=None, limit=None):
        if ip is not None:
            self.ip = ip
        if base is not None:
            self.base = base

        image = IntcodeImage(dict(program), ip=self.ip, base=self.base)
        max_addr = max(image.program)
        count = 0

        def write_line(*args, end='\n'):
            print(*args, end=end, file=self.output)

        def analysis(op):
            if not self.analyze: return ''
            s = op.analysis(image)
            return f'; {s}' if s else ''

        while image.ip <= max_addr and (limit is None or count < limit):
            op = _Operator.parse(image)

            if op is None:
                ip = image.ip
                image.ip = next((i for i in sorted(image.program) if i > ip), max_addr+1)
                continue

            asm = f'{image.ip:04}:  {op.assembly()}'
            lyz = analysis(op)
            if lyz:
                asm = f'{asm:<40}  {lyz}'
            write_line(asm)

            op.exec(image)
            count += 1

        self.ip = image.ip
        self.base = image.base


class _Param:
    ABSOLUTE, IMMEDIATE, RELATIVE = 0, 1, 2
    A, I, R = ABSOLUTE, IMMEDIATE, RELATIVE


class _Operator:
    known_ops = dict()

    @classmethod
    def register_op(cls, op):
        cls.known_ops[op.id] = op

    @classmethod
    def parse(cls, image):
        mem = image.program
        ip = image.ip

        op = mem.get(ip)
        if op is None: return

        klass = cls.known_ops.get(op % 100)

        if klass is None or any(mem.get(ip+i) is None for i in range(klass.size)):
            data = _Data()
            while klass is None or any(mem.get(ip+i) is None for i in range(klass.size)):
                data.append(op)
                if data.size == 8: break
                ip += 1
                op = mem.get(ip)
                if op is None: break
                klass = cls.known_ops.get(op % 100)
            return data

        r = klass()
        if klass.size > 1:
            r.mode1 = op // 100 % 10
            r.param1 = mem[ip + 1]
        if klass.size > 2:
            r.mode2 = op // 1000 % 10
            r.param2 = mem[ip + 2]
        if klass.size > 3:
            r.mode3 = op // 10000 % 10
            r.param3 = mem[ip + 3]
        return r

    def __init__(self):
        self.param1 = None
        self.param2 = None
        self.param3 = None
        self.mode1 = None
        self.mode2 = None
        self.mode3 = None

    def assembly(self):
        def ref(m, a):
            return (f'[base{a}]' if a < 0 else f'[base+{a}]') if (m == _Param.R) else (f'[{a}]' if m == 0 else str(a))
        return ''

    def analysis(self, image):
        pass

    def exec(self, image):
        image.ip += self.size

    def _format_param(self, mode, param):
        return (f'[base{param}]' if param < 0 else f'[base+{param}]') if (mode == _Param.R) else (f'[{param}]' if mode == _Param.A else str(param))

    @property
    def p1(self):
        return self._format_param(self.mode1, self.param1)

    @property
    def p2(self):
        return self._format_param(self.mode2, self.param2)

    @property
    def p3(self):
        return self._format_param(self.mode3, self.param3)

    def read_value(self, image, mode, param, default=0):
        mem = image.program
        return mem.get(image.base + param, default) if (mode == _Param.R) else (mem.get(param, default) if mode == _Param.A else param)

    def ref_value(self, image, mode, param):
        if mode == 1:
            raise Exception('referencing immediate value')
        return (image.base + param) if (mode == _Param.R) else param

    def value1(self, image):
        return self.read_value(image, self.mode1, self.param1)

    def value2(self, image):
        return self.read_value(image, self.mode2, self.param2)

    def value3(self, image):
        return self.read_value(image, self.mode3, self.param3)

    def ref1(self, image):
        return self.ref_value(image, self.mode1, self.param1)

    def ref2(self, image):
        return self.ref_value(image, self.mode2, self.param2)

    def ref3(self, image):
        return self.ref_value(image, self.mode3, self.param3)


def _knownop(cls):
    _Operator.register_op(cls)
    return cls


@_knownop
class _AddOp (_Operator):
    id = 1
    size = 4

    def assembly(self):
        return f'add {self.p3}, {self.p1}, {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        r = self.ref3(image)
        return f'[{r}] = {x + y} ({x} + {y})'

    def exec(self, image):
        mem = image.program
        mem[self.ref3(image)] = self.value1(image) + self.value2(image)
        super().exec(image)


@_knownop
class _MulOp (_Operator):
    id = 2
    size = 4

    def assembly(self):
        return f'mul {self.p3}, {self.p1}, {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        r = self.ref3(image)
        return f'[{r}] = {x * y} ({x} * {y})'

    def exec(self, image):
        mem = image.program
        mem[self.ref3(image)] = self.value1(image) * self.value2(image)
        super().exec(image)


@_knownop
class _InOp (_Operator):
    id = 3
    size = 2

    def assembly(self):
        return f'in {self.p1}'

    def analysis(self, image):
        r = self.ref1(image)
        return f'[{r}]'


@_knownop
class _OutOp (_Operator):
    id = 4
    size = 2

    def assembly(self):
        return f'out {self.p1}'

    def analysis(self, image):
        x = self.value1(image)
        return f'{x}'

@_knownop
class _JnzOp (_Operator):
    id = 5
    size = 3

    def assembly(self):
        return f'jnz {self.p1}, {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        if x:
            return f'jmp {y}'
        elif self.mode1 != _Param.I:
            r = self.ref1(image)
            return f'[{r}]: {x}'

@_knownop
class _JzOp (_Operator):
    id = 6
    size = 3

    def assembly(self):
        return f'jz {self.p1}, {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        if not x:
            return f'jmp {y}'
        elif self.mode1 != _Param.I:
            r = self.ref1(image)
            return f'[{r}]: {x}'


@_knownop
class _LtOp (_Operator):
    id = 7
    size = 4

    def assembly(self):
        return f'mov {self.p3}, {self.p1} < {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        r = self.ref3(image)
        v = 1 if x < y else 0
        return f'[{r}] = {v} ({x} < {y})'

    def exec(self, image):
        mem = image.program
        mem[self.ref3(image)] = 1 if self.value1(image) < self.value2(image) else 0
        super().exec(image)


@_knownop
class _EqOp (_Operator):
    id = 8
    size = 4

    def assembly(self):
        return f'mov {self.p3}, {self.p1} == {self.p2}'

    def analysis(self, image):
        x = self.value1(image)
        y = self.value2(image)
        r = self.ref3(image)
        v = 1 if x == y else 0
        return f'[{r}] = {v} ({x} == {y})'

    def exec(self, image):
        mem = image.program
        mem[self.ref3(image)] = 1 if self.value1(image) == self.value2(image) else 0
        super().exec(image)


@_knownop
class _BaseOp (_Operator):
    id = 9
    size = 2

    def assembly(self):
        return f'add base, {self.p1}'

    def analysis(self, image):
        x = self.value1(image)
        return f'{image.base + x}'

    def exec(self, image):
        image.base += self.value1(image)
        super().exec(image)


@_knownop
class _HaltOp (_Operator):
    id = 99
    size = 1

    def assembly(self):
        return f'hlt'


class _Data (_Operator):
    id = -1
    size = 0

    def __init__(self):
        self.data = list()
        self.size = 0

    def append(self, value):
        self.data.append(value)
        self.size += 1

    def assembly(self):
        s = ', '.join(map(str, self.data))
        return f'dw {s}'
