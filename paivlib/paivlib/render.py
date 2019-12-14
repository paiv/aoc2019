import itertools
import subprocess
import sys
from pathlib import Path
from PIL import Image


class FFMpeg:
    def __init__(self, output, size, rate=1):
        iw, ih = size
        quiet = '-y -hide_banner -loglevel error -nostats'
        audio = '-an'
        profile = '-codec:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset veryslow'
        if (iw % 2) or (ih % 2):
             profile += ' -vf scale=trunc(iw/2)*2:trunc(ih/2)*2'
        self.cmd = f'ffmpeg {quiet} -f rawvideo -s {iw}x{ih} -pix_fmt rgba -r {rate} -i - {audio} {profile} {output}'.split()
        self.proc = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        self.proc =  subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stderr=None)

    def close(self):
        if self.proc:
            self.proc.close()
            self.proc = None

    def write(self, data):
        try:
            self.proc.stdin.write(data)
        except BrokenPipeError:
            _, err = self.proc.communicate()
            print(err, file=sys.stderr)
            raise


class Sprites:
    def __init__(self, cwd=None, names=None):
        self.cwd = Path(cwd if cwd else '.')
        self.names = names

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __getitem__(self, key):
        return self.mapped[key]

    def open(self):
        def open_image(name):
            return Image.open(self.cwd / f'{name}.png').convert('RGBA')

        if not self.names:
            self.names = [s.stem for s in self.cwd.glob('*.png')]

        self.images = {s:open_image(s) for s in self.names}
        self.mapped = dict(self.images)
        self.size = next(iter(self.images.values())).size

    def close(self):
        for im in self.images.values():
            im.close()

    def remap(self, symbols, names):
        self.mapped = dict(zip(symbols, (self.images[s] for s in names)))


class VideoRenderer:
    def __init__(self, output=None, rate=1, scale=1, size=None, sprites=None):
        self.output = output
        self.rate = rate
        self.scale = scale
        self.sprites = sprites
        self.codec = None
        self.size = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        if self.size:
            self.codec = FFMpeg(self.output, size=self.size, rate=self.rate)
            self.codec.open()

    def close(self):
        if self.codec:
            self.codec.close()

    def render(self, frames):
        for frame in frames:
            with self._render_image(frame, self.scale) as im:
                if not self.codec:
                    self.size = im.size
                    self.open()
                data = im.tobytes()
                self.codec.write(data)

    def _render_image(self, frame, scale=1):
        rows = frame.splitlines()
        iw, ih = len(rows[0]), len(rows)
        stridex, stridey = self.sprites.size

        im = Image.new('RGBA', ((iw * stridex + 1) // 2 * 2, (ih * stridey + 1) // 2 * 2))

        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                s = self.sprites[c]
                im.paste(s, (x * stridex, y * stridey))

        if scale != 1:
            t, im = im, im.resize((iw*scale, ih*scale))
            t.close()
        return im
