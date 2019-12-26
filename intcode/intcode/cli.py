import argparse
import importlib
import readline
import sys
from . import IntcodeImage, IntcodeVM, IntcodeDisasm, DataDumper, IntcodeDebugger
from collections import deque


def assemble(args):
    pass


def disassemble(args):
    image = IntcodeImage.load(args.infile)
    dis = IntcodeDisasm(output=args.outfile)
    dis.process(image.program)


def raw_dump(args):
    dd = DataDumper(args.infile)
    dd.seek(args.seek)
    dd.dump(args.outfile)


def debugger(args):
    image = IntcodeImage.load(args.infile)
    ida = IntcodeDebugger()
    if args.driver:
        T = _load_class(args.driver)
        ida.driver = T()
    ida.load(image)
    ida.interactive()


def runner(args):
    image = IntcodeImage.load(args.infile)
    vm = IntcodeVM(image)
    if args.driver:
        T = _load_class(args.driver)
        driver = T()
    else:
        driver = _ConsoleDriver(ascii=args.ascii)
    vm.run(driver)


def _load_class(spec):
    m, n = spec.split(':')
    p = importlib.load_module(m)
    return getattr(p, n)


class _ConsoleDriver:
    def __init__(self, ascii=False):
        self.ascii = ascii
        self.output = None

    def is_active(self):
        return True

    def read(self):
        if self.output:
            return self.output.popleft()

        while True:
            text = input('> ')
            if not text: continue

            if self.ascii:
                self.output = deque(map(ord, f'{text}\n'))
                return self.output.popleft()

            else:
                try:
                    return int(text, base=0)
                except ValueError:
                    pass
                print(f'! error parsing integer: {repr(text)}', file=sys.stderr)

    def write(self, value):
        if self.ascii and 8 < value < 128:
            print(chr(value), end='', flush=True)
        else:
            print(repr(value))


def cli():
    parser = argparse.ArgumentParser(description='AoC 2019 Intcode VM Assembler')
    subparsers = parser.add_subparsers()

    asm = subparsers.add_parser('assemble', aliases=('a', 'asm'))
    asm.add_argument('infile', nargs='*', default=sys.stdin, type=argparse.FileType('r'),
        help='Input assembly')
    asm.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
        help='Write output to file')
    asm.add_argument('-g', '--generator', default='c', choices='c c-asm py'.split(),
        help='Select code generator')
    asm.set_defaults(handler=assemble)

    dis = subparsers.add_parser('disassemble', aliases=('d', 'dis', 'disasm'))
    dis.add_argument('infile', nargs='?', default=sys.stdin, type=argparse.FileType('r'),
        help='Input assembly')
    dis.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
        help='Write output to file')
    dis.set_defaults(handler=disassemble)

    dis = subparsers.add_parser('raw', aliases=('dd',))
    dis.add_argument('infile', nargs='?', default=sys.stdin, type=argparse.FileType('r'),
        help='Input assembly')
    dis.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
        help='Write output to file')
    dis.add_argument('-s', '--seek', default=0, type=int,
        help='Start at data offset')
    dis.set_defaults(handler=raw_dump)

    ida = subparsers.add_parser('debugger', aliases=('ida', 'debug'))
    ida.add_argument('infile', type=argparse.FileType('r'),
        help='Input assembly')
    ida.add_argument('-r', '--driver', default=None, type=str,
        help='Driver class, module:name')
    ida.set_defaults(handler=debugger)

    run = subparsers.add_parser('run', aliases=('r', 'exec'))
    run.add_argument('infile', type=argparse.FileType('r'),
        help='Input assembly')
    run.add_argument('-r', '--driver', default=None, type=str,
        help='Driver class, module:name')
    run.add_argument('-a', '--ascii', action='store_true',
        help='ASCII I/O')
    run.set_defaults(handler=runner)

    parser.add_argument('-v', '--verbose', action='store_true',
        help='print details')

    args = parser.parse_args()

    if not hasattr(args, 'handler'):
        parser.print_help()
        return

    args.handler(args)
