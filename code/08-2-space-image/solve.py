#!/usr/bin/env python
import paivlib as paiv


def solve(text, w=25, h=6):
    text = text.strip()
    frame = w * h
    layers = [text[i:i+frame] for i in range(0, len(text), frame)]

    image = [None]*frame
    for i in range(frame):
        px = None
        for layer in layers:
            t = layer[i]
            if t != '2':
                px = '#' if t == '1' else '.'
                break
        image[i] = px

    s = '\n'.join(''.join(image[i:i+w]) for i in range(0, frame, w))
    paiv.trace(s)


if __name__ == '__main__':
    print(solve(paiv.read_files()))
