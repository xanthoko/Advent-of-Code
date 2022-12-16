from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED_1 = 31
EXPECTED_2 = 29

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
        input_text = get_input_text(12)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')

    grid = {}
    start, end = None, None
    for r, row in enumerate(input_text.splitlines()):
        for c, col in enumerate(row):
            grid[(r, c)] = col
            if col == 'S':
                start = (r, c)
            if col == 'E':
                end = (r, c)
    return grid, start, end


grid, start, end = get_input_data()


def get_height(c: str):
    if c == 'S':
        return ord('a') - 1
    elif c == 'E':
        return ord('z') + 1
    return ord(c)


def get_steps(_start):
    visited = set()
    todo: list = [(0, _start[0], _start[1])]

    while todo:
        steps, row, col = todo.pop(0)
        if (row, col) in visited:
            continue
        visited.add((row, col))

        if (row, col) == end:
            return steps

        for dr, dc in (-1, 0), (1, 0), (0, -1), (0, 1):
            nr, nc = row + dr, col + dc
            if (nr, nc) not in grid:  # out of bounds
                continue
            if get_height(grid[
                (nr, nc)]) - get_height(grid[row, col]) > 1:  # too high
                continue
            todo.append((steps + 1, nr, nc))


def solve_1() -> int:
    return get_steps(start)


def solve_2() -> int:
    m = [get_steps(start)]
    for pos, el in grid.items():
        if el == 'a':
            if (s := get_steps(pos)) is not None:
                m.append(s)
    return min(m)


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
