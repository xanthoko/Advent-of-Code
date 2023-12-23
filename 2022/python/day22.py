from __future__ import annotations

import argparse

import numpy as np
from utils import get_input_text

EXAMPLE_INPUT = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
EXPECTED_1 = 6032
EXPECTED_2 = None

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
        input_text = get_input_text(22)
    else:
        input_text = EXAMPLE_INPUT
    input_text = input_text.strip('\n')
    map, instructions = input_text.split('\n\n')
    grid: dict[tuple[int, int], str] = {}
    for r, row in enumerate(map.splitlines()):
        for c, el in enumerate(row):
            if el != ' ':
                grid[(r, c)] = el

    i = 0
    ins = []
    cur = ''
    while i < len(instructions):
        if instructions[i].isdigit():
            cur += instructions[i]
        else:
            ins.append(int(cur))
            ins.append(instructions[i])
            cur = ''
        i += 1
    ins.append(int(cur))
    return grid, ins


input_data = get_input_data()
grid, instructions = input_data


def rotate(step: list[int], dir_cmd: str) -> list[int]:
    right_rm = [[0, -1], [1, 0]]
    left_rm = [[0, 1], [-1, 0]]
    if dir_cmd == 'L':
        return np.dot(step, left_rm)
    elif dir_cmd == 'R':
        return np.dot(step, right_rm)
    else:
        raise NotImplementedError(dir_cmd)


def get_next_pos(pos: list[int], step: list[int]) -> list[int]:
    next_pos = tuple([pos[0] + step[0], pos[1] + step[1]])
    # next_pos out of grid -> wrap around
    if next_pos not in grid:
        # moving horizontally
        if step[0] == 0:
            cands = [x for x, _ in grid.items() if x[0] == pos[0]]
            if step[1] == 1:
                # forward - look back
                next_pos = min(cands, key=lambda x: x[1])
            else:
                # backward - look front
                next_pos = max(cands, key=lambda x: x[1])
        else:  # move vertically
            assert step[1] == 0
            cands = [x for x, _ in grid.items() if x[1] == pos[1]]
            if step[0] == 1:
                # down - look up
                next_pos = min(cands, key=lambda x: x[0])
            else:
                # up - look down
                next_pos = max(cands, key=lambda x: x[0])
    return next_pos


def solve_1() -> int:
    step = [0, 1]
    pos = (0, 8)

    for instruction in instructions:
        if instruction in ['L', 'R']:
            step = rotate(step, instruction)
        else:
            for _ in range(instruction):
                next_pos = get_next_pos(pos, step)
                # check availability
                if grid[next_pos] == '#':
                    # stay in the same position
                    break
                else:
                    pos = next_pos
    if step[0] == 0 and step[1] == 1:
        f = 0
    elif step[0] == 0 and step[1] == -1:
        f = 2
    elif step[0] == 1 and step[1] == 0:
        f = 1
    else:
        f = 3
    return (pos[0] + 1) * 1000 + (pos[1] + 1) * 4 + f


def solve_2() -> int:
    # TODO: implement solution here
    pass


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
