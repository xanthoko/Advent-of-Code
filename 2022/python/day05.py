from __future__ import annotations

import argparse
from copy import deepcopy

from utils import get_input_text

EXAMPLE_INPUT = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED_1 = 'CMZ'
EXPECTED_2 = 'MCD'

parser = argparse.ArgumentParser(prog='AoC')
parser.add_argument('-p',
                    '--production',
                    required=False,
                    const=True,
                    nargs='?',
                    default=False)
is_production = parser.parse_args().production


def get_input_data() -> None:
    if is_production:
        input_text = get_input_text(5)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    initial, moves = input_text.split('\n\n')
    lines = initial.splitlines()
    no_stacks = len(lines[-1].split())
    stacks = [[] for _ in range(no_stacks)]

    for line in lines[:-1]:
        for i, c in enumerate(line[1::4]):
            if not c.isspace():
                stacks[i].insert(0, c)

    return stacks, moves


input_data = get_input_data()


def solve_1() -> str:
    stacks, moves = input_data
    stacks = deepcopy(stacks)

    for move in moves.splitlines():
        _, amount, _, src, _, dst = move.split(' ')
        amount = int(amount)
        src = int(src) - 1
        dst = int(dst) - 1

        for _ in range(amount):
            stacks[dst].append(stacks[src].pop())

    msg = ''
    for stack in stacks:
        msg += stack[-1]
    return msg


def solve_2() -> int:
    stacks, moves = input_data

    for move in moves.splitlines():
        _, amount, _, src, _, dst = move.split(' ')
        amount = int(amount)
        src = int(src) - 1
        dst = int(dst) - 1

        stacks[dst].extend(stacks[src][-amount:])
        stacks[src] = stacks[src][:-amount]

    msg = ''
    for stack in stacks:
        msg += stack[-1]
    return msg


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
