#!/usr/bin/env python
import intcode as ic
import io
import itertools
import paivlib as paiv
import re
import readline
from collections import deque


def solve(text):
    image = ic.IntcodeImage.loads(text)

    if 0:
        vm = ic.IntcodeVM(image)
        driver = Interact()
        vm.run(driver)
        return

    adventure = Adventure()
    adventure.ignore_items(*"""
infinite loop
giant electromagnet
photons
molten lava
escape pod
""".strip().splitlines())

    explorer = Explorer(adventure)
    while explorer.is_running():
        explorer.restart()
        vm = ic.IntcodeVM(image)
        vm.run(driver=explorer)

    return adventure.password


class Adventure:

    class Room:
        def __init__(self, name=None):
            self.name = name
            self.exits = dict()
            self.items = list()
            self.description = None
        def __repr__(self):
            exits = {k:(v.name if v else v) for k, v in self.exits.items()}
            return f'({repr(self.name)}, {exits}, {self.items})'
        def __hash__(self):
            return hash(self.name)
        def __eq__(self, other):
            return (self.name is not None) and (self.name == other.name)
        @property
        def is_blank(self):
            return self.name is None
        def update_exit(self, door):
            for p, child in self.exits.items():
                if door == child:
                    d = dict(door.exits)
                    d.update(child.exits)
                    chld.exits = d
                    child.items = door.items
                    break

    def __init__(self):
        self.state = 0
        self.root = None
        self.pos = None
        self.move = None
        self.visited = set()
        self.rooms = dict()
        self.ignore = set()
        self.collected = list()
        self.stay_away = set(['Security Checkpoint'])
        self.pending_actions = deque()
        self.path = None
        self.last_move = None
        self.password = None

    @property
    def is_complete(self):
        return self.state == -1

    def ignore_items(self, *items):
        if items:
            self.ignore |= set(items)

    def restart(self):
        self.pos = None
        self.pending_actions = deque()
        self.path = None

    def consume(self, text):
        room = self.parse(text)
        if room:
            self._visit_room(room)

        elif self.state == 1 and 'keypad' in text:
            self.password, = re.findall(r'\d+', text)
            self.state = -1

    def _visit_room(self, room):
        self.pos = room
        if self.root is None: self.root = self.pos
        self.rooms[room.name] = room
        self.pending_actions = deque()

        if self.path:
            _,p = self.path[0]
            if p is None or p == self.pos:
                self.path.popleft()
                prev, act = self.last_move
                prev.exits[act.strip()] = room

                if room.name in self.stay_away:
                    prev, act = self.last_move
                    wasd = 'north\n west\n south\n east\n'.split(' ')
                    back = dict(zip(wasd, wasd[2:]+wasd[:2]))[act]
                    self.pending_actions.append(back)
                    return
            else:
                self.path = None

        take = [i for i in room.items if i not in self.ignore]
        if take:
            self.collected.extend(take)
            take = [self.take(i) for i in take]
            self.pending_actions = deque(take)

    def do_action(self):
        if self.state == -1: return

        if self.pending_actions:
            return self.pending_actions.popleft()

        if self.path:
            prev, (act, self.pos) = self.pos, self.path[0]
            self.pending_actions.append(act)
            self.last_move = (prev, act)
            return self.do_action()

        if self.state == 0:
            path = self._next_unexplored(safe=True)
            if path:
                self.path = deque(path[1:])
                return self.do_action()
            else:
                self.state = 1
                self.stay_away = set()
                return self.do_action()

        elif self.state == 1 and not self.pos:
            self.state = -1

        elif self.state == 1:
            if self.pos.name == 'Security Checkpoint':
                self.pending_actions = deque(self._bruteforce_items())
            else:
                path = self._next_unexplored(safe=False)
                if path:
                    self.path = deque(path[1:-1])
                    return self.do_action()
                else:
                    self.state = -1

    def _bruteforce_items(self):
        have = self.collected
        for take in itertools.product([0,1], repeat=len(have)):
            take = set(i for i,x in zip(have, take) if x)
            p = ''.join(f'drop {i}\n' for i in have if i not in take)
            p += 'north\n'
            p += ''.join(f'take {i}\n' for i in have if i not in take)
            yield p

    def parse(self, text):
        text = text.strip()
        if text.startswith('=='):
            return self.parse_room(text)

    def take(self, item):
         return f'take {item}\n'

    def drop(self, item):
         return f'drop {item}\n'

    def parse_room(self, text):
        name = self.parse_room_name(text)
        doors = self.parse_room_exits(text)
        items = self.parse_room_items(text)
        r = self.rooms.get(name)
        if r:
            exits = dict((i, None) for i in doors)
            exits.update(r.exits)
            r.exits = exits
        else:
            r = Adventure.Room(name)
            r.exits = dict((i, None) for i in doors)
        r.items = items
        return r

    def parse_room_name(self, text):
        xs = re.findall(r'== (.+?) ==', text)
        if xs: return xs[0]

    def parse_room_exits(self, text):
        xs = re.findall(r'Doors here lead:(\n-.*?)\n\n', text, re.S)
        return self._parse_list(xs[0]) if xs else list()

    def parse_room_items(self, text):
        xs = re.findall(r'Items here:(\n-.*?)\n\n', text, re.S)
        return self._parse_list(xs[0]) if xs else list()

    def _parse_list(self, text):
        return re.findall(r'\n- ([^\n]+)', text, re.S) if text else list()

    def _next_unexplored(self, safe=True):
        class Node:
            def __init__(self, door, pos, parent=None):
                self.door = door
                self.pos = pos
                self.parent = parent
            def __repr__(self):
                return f'Node({self.door}, {self.pos} |{self.parent}|)'
            def __hash__(self):
                return hash((self.door, self.pos))
            def __eq__(self, other):
                return (self.door == other.door) and (self.pos == other.pos)
            def path(self):
                p = [(f'{self.door}\n' if self.door else None, self.pos)]
                return (p if (self.parent is None) else (self.parent.path() + p))

        start = Node(None, self.pos)
        fringe = deque([start])
        visited = set()

        while fringe:
            node = fringe.popleft()
            if node.pos is None:
                return node.path()
            if node in visited: continue
            visited.add(node)
            room = self.rooms[node.pos.name]
            for t, child in room.exits.items():
                if (child is None) or (not safe) or (child.name not in self.stay_away):
                    fringe.append(Node(t, child, parent=node))


class Explorer:
    def __init__(self, adventure):
        self.output = None
        self.input = None
        self.active = True
        self.adventure = adventure

    def is_running(self):
        return not self.adventure.is_complete

    def is_active(self):
        return self.active

    def read(self):
        if not self.output:

            if self.input:
                text = ''.join(map(chr, self.input))
                self.input = list()
                self.adventure.consume(text)

            act = self.adventure.do_action()
            if not act:
                self.active = not self.adventure.is_complete
                return 0

            self.output = deque(act)

        s = self.output.popleft()
        return ord(s)

    def write(self, value):
        if not self.input:
            self.input = list()
        self.input.append(value)

    def restart(self):
        self.adventure.restart()


class Interact:
    def __init__(self):
        self.output = None
        self.hotkeys = {
            'n': 'north',
            'w': 'west',
            's': 'south',
            'e': 'east',
            'i': 'inv',
        }

    def is_active(self):
        return True

    def read(self):
        if not self.output:
            s = input('> ')
            cmd = self.hotkeys.get(s, s)
            self.output = deque(cmd + '\n')
        s = self.output.popleft()
        return ord(s)

    def write(self, value):
        if 9 <= value < 128:
            print(chr(value), end='')
        else:
            print(repr(value))


if __name__ == '__main__':
    print(solve(paiv.read_files()))
