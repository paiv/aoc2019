import io
from .vm import IntcodeImage


class DataDumper:
    def __init__(self, infile):
        im = IntcodeImage.load(infile)
        self.data = list(im.program)
        self.offset = 0

    def seek(self, offset):
        self.offset = offset

    def dump(self, output):
        so = output or io.StringIO()

        def write_line(*args, end='\n'):
            print(*args, end=end, file=so)

        o = self.offset
        for i in range(self.offset, len(self.data), 8):
            s = ', '.join(map(str, self.data[i:i+8]))
            write_line(f'{o:05}:', end=' ')
            write_line(f'dw {s}')
            o += 8

        if hasattr(so, 'getvalue'):
            return so.getvalue()
        return so
