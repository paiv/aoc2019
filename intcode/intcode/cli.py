import argparse
import importlib
import sys
from . import IntcodeImage, IntcodeDisasm, DataDumper, IntcodeDebugger


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


def _load_class(spec):
    m, n = spec.split(':')
    p = importlib.load_module(m)
    return getattr(p, n)


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

    parser.add_argument('-v', '--verbose', action='store_true',
        help='print details')

    args = parser.parse_args()

    if not hasattr(args, 'handler'):
        parser.print_help()
        return

    args.handler(args)
