from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED_1 = 95437
EXPECTED_2 = 24933642

parser = argparse.ArgumentParser(prog='AoC')
parser.add_argument('-p',
                    '--production',
                    required=False,
                    const=True,
                    nargs='?',
                    default=False)
is_production = parser.parse_args().production


class Directory:

    def __init__(self, name: str, parent: Directory = None) -> None:
        self.name: str = name
        self.size: int = 0
        self.children: dict[str, Directory] = {}
        self.parent: Directory = parent

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


def get_input_data() -> None:
    if is_production:
        input_text = get_input_text(7)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')

    cur = root = Directory('/')

    for cmd in input_text.splitlines()[1:]:
        splt = cmd.split(' ')

        if splt[1] == 'cd':
            dst = splt[2]
            if dst == '..':
                cur = cur.parent
            else:
                if dst in cur.children:
                    cur = cur.children[dst]
                else:
                    child = Directory(dst, cur)
                    cur.children[dst] = child
                    cur = child
        elif splt[1] == 'ls':
            continue
        else:
            if splt[0] != 'dir':
                cur.size += int(splt[0])
    return root


input_data: Directory = get_input_data()


def solve_1() -> int:
    ret = 0

    def parse_tree(node: Directory) -> int:
        nonlocal ret
        if not node.children:
            if node.size < 100000:
                ret += node.size
            return node.size

        # parse children
        for _, child in node.children.items():
            node.size += parse_tree(child)

        if node.size < 100000:
            ret += node.size
        return node.size

    parse_tree(input_data)

    return ret


def solve_2() -> int:
    avail = 70000000
    needed = 30000000
    used = input_data.size
    unused = avail - used
    targ = needed - unused
    cands = used

    def parse_tree(node: Directory) -> int:
        nonlocal cands
        if not node.children:
            if node.size > targ:
                cands = min(cands, node.size)
            return

        # parse children
        for _, child in node.children.items():
            parse_tree(child)

        if node.size > targ:
            cands = min(cands, node.size)
        return node.size

    parse_tree(input_data)
    return cands


def _validate(expected, actual):
    if not is_production:
        error_msg = f'\033[41mExpected: {expected}. Got: {actual}\033[m'
        assert actual == expected, error_msg


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')
    _validate(EXPECTED_1, part_1)

    part_2 = solve_2()
    print(f'Part 2: {part_2}')
    _validate(EXPECTED_2, part_2)


if __name__ == '__main__':
    solve()
