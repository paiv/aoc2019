#!/usr/bin/env python -OO
import heapq
import paivlib as paiv
import string
import time
from collections import deque


def solve(text):
    grid = dict((x + 1j*y, c)
        for y, row in enumerate(text.strip().splitlines())
        for x, c in enumerate(row))

    pos = next(k for k, c in grid.items() if c == '@')
    grid[pos] = '.'

    any_key = set(string.ascii_lowercase)
    all_keys = dict((c, k) for k, c in grid.items() if c in any_key)

    any_door = set(string.ascii_uppercase)
    all_doors = dict((c, k) for k, c in grid.items() if c in any_door)

    paiv.trace(pos, all_keys, all_doors)

    found, path = find_plan(grid, pos, all_keys, all_doors)
    paiv.trace(path, found)
    return path


class PlanItem:
    def __init__(self, start, pos, found='', path=0):
        self.start = start
        self.pos = pos
        self.found = found
        self.path = path
        self.weight = (self.path, -len(self.found))
        self.comp = (self.start, ''.join(sorted(self.found)))

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.comp == other.comp

    def __hash__(self):
        return hash(self.comp)


def find_plan(grid, pos, keys, doors):
    goal = len(keys)
    fringe = [PlanItem(pos, pos)]
    visited = set()
    tlast = time.monotonic()
    while fringe:
        node = heapq.heappop(fringe)
        if len(node.found) == goal: return (node.found, node.path)
        if node in visited: continue
        visited.add(node)

        now = time.monotonic()
        if now - tlast > 2:
            paiv.trace(node.found, len(fringe))
            tlast = now

        ks = reachable_keys(grid, node.pos, node.found)
        for k, p, n in ks:
            heapq.heappush(fringe, PlanItem(node.pos, p, node.found + k, node.path + n))


def reachable_keys(grid, pos, found):
    clear = found.upper() + found
    fringe = deque([pos])
    visited = {pos: 0}
    moves = (-1j, -1, 1j, 1)
    reachable = list()
    while fringe:
        start = fringe.popleft()
        for t in moves:
            pos = start + t

            if pos in visited: continue
            n = visited[pos] = visited[start] + 1

            k = grid.get(pos)
            if k and k != '#':
                if k.isupper() and k not in clear:
                    continue
                elif k.islower() and k not in clear:
                    reachable.append((k, pos, n))
                else:
                    fringe.append(pos)
    return reachable


def test():
    paiv.test_subject(solve)

    s = """
#########
#b.A.@.a#
#########
"""
    paiv.test(s) == 8

    s = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
    paiv.test(s) == 86

    s = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
    paiv.test(s) == 132

    s = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
    paiv.test(s) == 136

    s = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
    paiv.test(s) == 81


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
