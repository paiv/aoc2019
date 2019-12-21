#!/usr/bin/env python
import heapq
import itertools
import paivlib as paiv
import string
import time
from collections import deque


def solve(text):
    grid = dict((x + 1j*y, c)
        for y, row in enumerate(text.strip().splitlines())
        for x, c in enumerate(row))

    pos = next(k for k, c in grid.items() if c == '@')
    for t in (-1j , -1, 0, 1j, 1):
        grid[pos + t] = '#'
    start = [pos + t for t in (1-1j, -1-1j, -1+1j, 1+1j)]

    any_key = set(string.ascii_lowercase)
    all_keys = dict((c, k) for k, c in grid.items() if c in any_key)

    any_door = set(string.ascii_uppercase)
    all_doors = dict((c, k) for k, c in grid.items() if c in any_door)

    paiv.trace(start, all_keys, all_doors)

    found, path = find_plan(grid, start, all_keys, all_doors)
    paiv.trace(path, found)
    return path


class PlanItem:
    def __init__(self, start, pos, found='', path=0):
        self.start = start
        self.pos = pos
        self.found = found
        self.path = path
        self.weight = (self.path, -len(self.found))
        self.comp = (tuple(sorted((p.imag, p.real) for p in self.start)), ''.join(sorted(self.found)))

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.comp == other.comp

    def __hash__(self):
        return hash(self.comp)


def find_plan(grid, start, keys, doors):
    goal = len(keys)
    fringe = [PlanItem(start, start)]
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

        for item in reachable_keys2(grid, node):
            paiv.trace(' ', item.start, item.pos, item.found, item.path)
            heapq.heappush(fringe, item)


def reachable_keys2(grid, node):
    ks = [reachable_keys(grid, start, node.found) for start in node.pos]
    for ps in itertools.product(*filter(None, ks)):
        start = [p[0] for p in ps]
        pos = [p[1] for p in ps]
        ks = ''.join(p[2] for p in ps)
        n = sum(p[3] for p in ps)
        yield PlanItem(start, pos, node.found + ks, node.path + n)


def reachable_keys(grid, start, found):
    clear = found.upper() + found
    fringe = deque([start])
    visited = {start: 0}
    moves = (-1j, -1, 1j, 1)
    reachable = list()
    while fringe:
        pos = fringe.popleft()
        for t in moves:
            xto = pos + t

            if xto in visited: continue
            n = visited[xto] = visited[pos] + 1

            k = grid.get(xto)
            if k and k != '#':
                if k.isupper() and k not in clear:
                    continue
                elif k.islower() and k not in clear:
                    reachable.append((start, xto, k, n))
                else:
                    fringe.append(xto)
    return reachable


def test():
    paiv.test_subject(solve)

    s = """
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
"""
    paiv.test(s) == 8

    s = """
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
"""
    paiv.test(s) == 24

    s = """
#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
"""
    paiv.test(s) == 32

    s = """
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
"""
    paiv.test(s) == 72


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
