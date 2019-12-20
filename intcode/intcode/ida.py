import io
import readline
import signal
from .disasm import IntcodeDisasm
from .vm import IntcodeDebugVM


class IntcodeDebugger:
    def __init__(self, image=None):
        self.image = image
        self.vm = None
        self.driver = _IODriver(self)
        self.last_command = None
        self.commands = {
            _Command.BREAK: self._cmd_breakpoint,
            _Command.CONTINUE: self._cmd_continue,
            _Command.HELP: self._cmd_help,
            _Command.MEMORY: self._cmd_memory,
            _Command.NEXT: self._cmd_next,
            _Command.QUIT: self._cmd_quit,
            _Command.REPEAT: self._cmd_repeat_last,
            _Command.RUN: self._cmd_run,
            _Command.STEP: self._cmd_next,
        }

    def load(self, image):
        self.image = image

    def interactive(self):
        self.quit_interactive = False
        while not self.quit_interactive:
            cmd = self.user_input()
            cmd = _Command.parse(cmd)
            self._dispatch_command(cmd)

    def user_input(self, prompt=None):
        if prompt is None: prompt = 'ida> '
        sig = signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            return input(f'{prompt}')
        except EOFError:
            pass
        signal.signal(signal.SIGINT, sig)

    def user_print(self, text):
        print(text, flush=True)

    def _dispatch_command(self, cmd):
        handler = self.commands.get(cmd.name)
        if handler is None:
            self.user_print(f'! unhandled: {cmd}')
            self.user_print(f'usage: ?')
        else:
            handler(*cmd.args)

        if cmd.name != _Command.REPEAT:
            self.last_command = cmd

    def _cmd_help(self, *args):
        cmd = _Command(_Command.HELP)
        self.user_print(cmd.usage())

    def _cmd_repeat_last(self, *args):
        if self.last_command:
            self._dispatch_command(self.last_command)

    def _cmd_quit(self, *args):
        self.quit_interactive = True

    def _cmd_run(self, *args):
        image = self.image.copy()
        oldvm = self.vm
        self.vm = IntcodeDebugVM(image, self.driver)
        self.vm.debugger = self
        if oldvm:
            self.vm.update_breakpoints(oldvm.breakpoints)
        self.vm.run()
        self._stop_hook()

    def _cmd_breakpoint(self, *args):
        if not self._check_vm_running_or_none(start=False):
            return

        bps = self.vm.breakpoints
        if not args:
            for id, (kind, val) in bps.items():
                if kind == 'ip':
                    spec = f'break at {val}'
                else:
                    spec = f'({kind} {val})'
                self.user_print(f'{id}: {spec}')
        else:
            image = self.vm.image
            base = image.base
            def addr(s):
                if s == 'base': return base
                return int(s, base=0)
            for i in map(addr, args):
                self.vm.add_ip_break(i)

    def _cmd_continue(self, *args):
        if not self._check_vm_running_or_none():
            return
        self.vm.run()
        self._stop_hook()

    def _cmd_next(self, *args):
        if not self._check_vm_running_or_none():
            return
        self.vm.single_step()
        self._stop_hook()

    def _check_vm_running_or_none(self, start=True):
        if self.vm is None and start:
            self._cmd_run()
            return self._check_vm_running_or_none(start=False)
        elif self.vm is None:
            self.user_print(f'! not running')
            return False
        elif not self.vm.running:
            self.user_print(f': process terminated')
            return False
        return True

    def _stop_hook(self):
        if not self._check_vm_running_or_none(start=False):
            return

        image = self.vm.image

        self.user_print('--')
        self.user_print(f'base={image.base}')
        self._dump_changed_memory()

        dis = IntcodeDisasm(analyze=True)
        dis.process(image.program, ip=image.ip, base=image.base, limit=3)
        asm = dis.output.getvalue()
        self.user_print(asm)

    def _dump_changed_memory(self):
        diff = self.vm.changed_memory
        if not diff: return

        def group(xs):
            state = 0
            r = list()
            for x in sorted(xs):
                if state == 0:
                    r.append(x)
                    state = 1
                elif state == 1 and len(r) < 8 and x - r[-1] == 1:
                    r.append(x)
                else:
                    yield r
                    r = list()
                    state = 0
            if r: yield r

        so = io.StringIO()
        for g in group(diff):
            off = g[0]
            s = ', '.join(map(str, (diff[k] for k in g)))
            so.write(f'{off:04}: {s}\n')
        self.user_print(so.getvalue())

    def _cmd_memory(self, *args):
        if not self._check_vm_running_or_none(start=False):
            return

        image = self.vm.image
        mem = image.program
        base = image.base

        def addr(s):
            if not s: return []
            n = 1
            if ':' in s:
                i, j = map(addr, s.split(':'))
                i = 0 if not i else i[0]
                n = j[0] - i
            elif s == 'base':
                i = base
            else:
                i = int(s, base=0)
            return [*range(i, i + n)]

        def read(ix):
            return [mem.get(k,0) for k in ix]

        for ks in filter(None, map(addr, args)):
            for i in range(0, len(ks), 8):
                ix = ks[i:i+8]
                i = ix[0]
                self.user_print(f'{i:04}: ' + ', '.join(map(str, read(ix))))


class _Command:
    BREAK = 'break'
    CONTINUE = 'continue'
    HELP = 'help'
    MEMORY = 'memory'
    NEXT = 'next'
    REPEAT = '!!'
    RUN = 'run'
    STEP = 'step'
    QUIT = 'quit'

    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __str__(self):
        return ' '.join(type(self.args)([self.name]) + self.args)

    def parse(text):
        if text is None:
            return _Command(_Command.QUIT)

        args = text.split()
        name, args = ''.join(args[:1]), args[1:]

        alias = {
            '': _Command.REPEAT,
            '?': _Command.HELP,
            'b': _Command.BREAK,
            'br': _Command.BREAK,
            'c': _Command.CONTINUE,
            'm': _Command.MEMORY,
            'mem': _Command.MEMORY,
            'n': _Command.NEXT,
            'q': _Command.QUIT,
            's': _Command.STEP,
        }

        return _Command(alias.get(name, name), *args)

    def usage(self):
        if self.name == self.HELP:
            return """commands:
run
c, continue
n, next
s, step
b, break [addr]
m, memory [addr]
!!, repeat
?, help
q, quit
"""


class _IODriver:
    def __init__(self, debugger):
        self.debugger = debugger
        self.active = True

    def is_active(self):
        return self.active

    def read(self):
        while True:
            text = self.debugger.user_input('ic# ')
            if not text: continue
            try:
                return int(text, base=0)
            except ValueError:
                pass
            raise ValueError(repr(text))

    def write(self, value):
        self.debugger.user_print(repr(value))
