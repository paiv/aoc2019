#!/usr/bin/env python
import heapq
import paivlib as paiv
from collections import defaultdict, deque


def solve(text):
    grid = dict((x + 1j * y, c)
        for y, row in enumerate(text.strip('\n').splitlines())
        for x, c in enumerate(row)
        if not c.isspace())

    wasd = (-1j, -1, 1j, 1)

    def label(p):
        for t in wasd:
            if grid.get(p + t, '').isalpha():
                aa = grid[p+t] + grid[p+t+t]
                if t in (-1j, -1):
                    aa = aa[::-1]
                return aa

    telepads = dict((p, label(p))
        for p, c in grid.items()
        if c == '.'
        if any(grid.get(p+t, '').isalpha() for t in wasd))
    paiv.trace('pads:', telepads)

    AA = next(p for p, a in telepads.items() if a == 'AA')
    ZZ = next(p for p, a in telepads.items() if a == 'ZZ')
    paiv.trace('AA:', AA, 'ZZ:', ZZ)

    xs = [p.real for p, c in grid.items() if c == '.']
    minx, maxx = min(xs), max(xs)
    ys = [p.imag for p, c in grid.items() if c == '.']
    miny, maxy = min(ys), max(ys)

    portals = dict((p, q)
        for p, a in telepads.items()
        for q, b in telepads.items()
        if a == b
        if p != q)
    # paiv.trace(portals)

    edges = find_paths(grid, set(telepads))
    for p, q in portals.items():
        edges[p,q] = 1
        edges[q,p] = 1
    # paiv.trace(edges)

    graph = defaultdict(set)
    for p, q in edges:
        graph[p].add(q)
        graph[q].add(p)
    # paiv.trace(graph)

    # 1 inner, -1 outer
    elevator = defaultdict(lambda: defaultdict(int))
    for a, b in portals.items():
        for t in wasd:
            q = a + t
            if grid[q].isalpha():
                z = q.real > maxx or q.real < minx or q.imag > maxy or q.imag < miny
                elevator[a][b] = -1 if z else 1
                elevator[b][a] = 1 if z else -1
                break
    # paiv.trace(elevator)

    n, path = find_path(graph, edges, AA, ZZ, elevator)
    paiv.print_stderr(n, ''.join(telepads[p] + f'-{edges[(p,q)]}-' for p,q in zip(path, path[1:])) + 'ZZ')
    return n


def find_paths(grid, pois):

    class PathNode:
        def __init__(self, pos, weight=0, root=None):
            self.pos = pos
            self.weight = weight
            self.root = root or pos

        def __hash__(self):
            return hash((self.root, self.pos))

        def __eq__(self, other):
            return (self.root == other.root) and (self.pos == other.pos)

        def __lt__(self, other):
            return (self.weight < other.weight)

    fringe = [PathNode(p) for p in pois]
    visited = set()
    wasd = (-1j, -1, 1j, 1)
    while fringe:
        node = heapq.heappop(fringe)
        if node in visited: continue
        visited.add(node)
        if node.pos in pois:
            visited.add(PathNode(node.root, node.weight, root=node.pos))
        for t in wasd:
            xto = node.pos + t
            if grid.get(xto) == '.':
                heapq.heappush(fringe, PathNode(xto, node.weight + 1, node.root))

    dist = dict(((n.root, n.pos), n.weight) for n in visited if n.root in pois if n.pos in pois)
    return dist


def find_path(graph, edges, start, goal, elevator):

    class PathNode:
        def __init__(self, pos, level=0, weight=0, parent=None):
            self.pos = pos
            self.level = level
            self.weight = weight
            self.parent = parent

        def __hash__(self):
            return hash((self.pos, self.level))

        def __eq__(self, other):
            return (self.pos == other.pos) and (self.level == other.level)

        def __lt__(self, other):
            return (self.weight < other.weight) or ((self.weight == other.weight) and (self.level < other.level))

        def path(self):
            p = [] if self.parent is None else self.parent.path()
            p.append(self.pos)
            return p

    fringe = [PathNode(start)]
    visited = defaultdict(set)
    while fringe:
        node = heapq.heappop(fringe)
        if node.pos == goal:
            return (node.weight, node.path())
        if node in visited[node.level]: continue
        visited[node.level].add(node)

        for xto in graph[node.pos]:
            xl = node.level + elevator[node.pos][xto]
            if xl < 0: continue
            if node.level != 0 and (xto == start or xto == goal):
                continue
            n = edges[(node.pos, xto)]
            heapq.heappush(fringe, PathNode(xto, xl, node.weight + n, parent=node))


def test():
    paiv.test_subject(solve)

    s = """
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
"""
    paiv.test(s) == 26

    s = """
             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M
"""
    paiv.test(s) == 396


if __name__ == '__main__':
    test()
    print(solve(paiv.read_files()))
