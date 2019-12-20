import io


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

        mem = program
        ip = self.ip
        base = self.base
        max_addr = max(mem)
        count = 0

        def write_line(*args, end='\n'):
            print(*args, end=end, file=self.output)

        def analysis(op):
            if not self.analyze: return ''
            s = op.analysis(mem, base=base)
            return f'; {s}' if s else ''

        while ip <= max_addr and (limit is None or count < limit):
            op = _Operator.parse(mem, ip)

            if op is None:
                ip = next((i for i in sorted(mem) if i > ip), max_addr+1)
                continue

            asm = f'{ip:04}:  {op.assembly()}'
            lyz = analysis(op)
            if lyz:
                asm = f'{asm:<40}  {lyz}'
            write_line(asm)

            ip += op.size
            count += 1

            if op.id == _BaseOp.id:
                base += op.value1(mem, base)

        self.ip = ip
        self.base = base


class _Operator:
    known_ops = dict()

    @classmethod
    def register_op(cls, op):
        cls.known_ops[op.id] = op

    @classmethod
    def parse(cls, mem, ip):
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
            return (f'[base{a}]' if a < 0 else f'[base+{a}]') if (m == 2) else (f'[{a}]' if m == 0 else str(a))
        return ''

    def _format_param(self, mode, param):
        return (f'[base{param}]' if param < 0 else f'[base+{param}]') if (mode == 2) else (f'[{param}]' if mode == 0 else str(param))

    @property
    def p1(self):
        return self._format_param(self.mode1, self.param1)

    @property
    def p2(self):
        return self._format_param(self.mode2, self.param2)

    @property
    def p3(self):
        return self._format_param(self.mode3, self.param3)

    def analysis(self, mem, base=0):
        pass

    def read_value(self, mem, base, mode, param, default=0):
        return mem.get(base + param, default) if (mode == 2) else (mem.get(param, default) if mode == 0 else param)

    def ref_value(self, mem, base, mode, param):
        return f'[{base + param}]' if (mode == 2) else (f'[{param}]' if mode == 0 else f'{param}')

    def value1(self, mem, base=0):
        return self.read_value(mem, base, self.mode1, self.param1)

    def value2(self, mem, base=0):
        return self.read_value(mem, base, self.mode2, self.param2)

    def value3(self, mem, base=0):
        return self.read_value(mem, base, self.mode3, self.param3)

    def ref1(self, mem, base=0):
        return self.ref_value(mem, base, self.mode1, self.param1)

    def ref2(self, mem, base=0):
        return self.ref_value(mem, base, self.mode2, self.param2)

    def ref3(self, mem, base=0):
        return self.ref_value(mem, base, self.mode3, self.param3)


def _knownop(cls):
    _Operator.register_op(cls)
    return cls


@_knownop
class _BaseOp (_Operator):
    id = 9
    size = 2

    def assembly(self):
        return f'add base, {self.p1}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        return f'{base + x}'


@_knownop
class _AddOp (_Operator):
    id = 1
    size = 4

    def assembly(self):
        return f'add {self.p3}, {self.p1}, {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref3(mem, base)
        return f'{r} = {x + y} ({x} + {y})'


@_knownop
class _MulOp (_Operator):
    id = 2
    size = 4

    def assembly(self):
        return f'mul {self.p3}, {self.p1}, {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref3(mem, base)
        return f'{r} = {x * y} ({x} * {y})'


@_knownop
class _InOp (_Operator):
    id = 3
    size = 2

    def assembly(self):
        return f'in {self.p1}'

    def analysis(self, mem, base=0):
        r = self.ref1(mem, base)
        return f'{r}'


@_knownop
class _OutOp (_Operator):
    id = 4
    size = 2

    def assembly(self):
        return f'out {self.p1}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        return f'{x}'

@_knownop
class _JnzOp (_Operator):
    id = 5
    size = 3

    def assembly(self):
        return f'jnz {self.p1}, {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref1(mem, base)
        if x: return f'jmp {y}'
        else: return f'{r}: {x}'

@_knownop
class _JzOp (_Operator):
    id = 6
    size = 3

    def assembly(self):
        return f'jz {self.p1}, {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref1(mem, base)
        if x == 0: return f'jmp {y}'
        else: return f'{r}: {x}'


@_knownop
class _LtOp (_Operator):
    id = 7
    size = 4

    def assembly(self):
        return f'mov {self.p3}, {self.p1} < {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref3(mem, base)
        v = 1 if x < y else 0
        return f'{r} = {v} ({x} < {y})'


@_knownop
class _EqOp (_Operator):
    id = 8
    size = 4

    def assembly(self):
        return f'mov {self.p3}, {self.p1} == {self.p2}'

    def analysis(self, mem, base=0):
        x = self.value1(mem, base)
        y = self.value2(mem, base)
        r = self.ref3(mem, base)
        v = 1 if x == y else 0
        return f'{r} = {v} ({x} == {y})'


@_knownop
class _HaltOp (_Operator):
    id = 99
    size = 1

    def assembly(self):
        return f'hlt'


class _Data:
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

    def analysis(self, mem, base=0):
        pass
