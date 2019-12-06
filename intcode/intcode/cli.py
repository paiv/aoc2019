import argparse
import sys
from . import IntcodeImage, IntcodeDisasm


def assemble(args):
    pass


def disassemble(args):
    image = IntcodeImage.load(args.infile)
    dis = IntcodeDisasm()
    dis.process(image, output=args.outfile)


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

    parser.add_argument('-v', '--verbose', action='store_true',
        help='print details')

    args = parser.parse_args()

    if not hasattr(args, 'handler'):
        parser.print_help()
        return

    args.handler(args)
