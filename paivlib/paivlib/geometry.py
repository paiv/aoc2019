import math


def l1_distance(a, b):
    if isinstance(a, complex):
        return abs(b.real - a.real) + abs(b.imag - a.imag)
    elif isinstance(a, tuple):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    raise Exception(f'{type(a)} {type(b)}')

l1_dist = l1_distance
manhattan_distance = l1_distance


def l2_distance(a, b):
    if isinstance(a, complex):
        return math.sqrt((b.real - a.real) ** 2 + (b.imag - a.imag) ** 2)
    elif isinstance(a, tuple):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    raise Exception(f'{type(a)} {type(b)}')

l2_dist = l2_distance
euclidean_distance = l2_distance


def line_through_points(a, b):
    ax, ay = a
    bx, by = b
    if ax == bx:
        return (ax, None)
    m = ((by - ay) / (bx - ax))
    n = (by - m * bx)
    return (m, n)
