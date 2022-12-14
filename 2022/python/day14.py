from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED_1 = 24
EXPECTED_2 = 93

parser = argparse.ArgumentParser(prog='AoC')
parser.add_argument('-p',
                    '--production',
                    required=False,
                    const=True,
                    nargs='?',
                    default=False)
is_production = parser.parse_args().production


def get_input_data() -> set(tuple(int, int)):
    if is_production:
        input_text = get_input_text(14)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')

    rocks: set(tuple(int, int)) = set()
    for path in input_text.splitlines():
        edges = [list(map(int, x.split(','))) for x in path.split(' -> ')]
        for i in range(1, len(edges)):
            c, p = edges[i], edges[i - 1]
            if c[0] == p[0]:
                for j in range(min(c[1], p[1]), max(c[1], p[1]) + 1):
                    rocks.add((c[0], j))
            elif c[1] == p[1]:
                for j in range(min(c[0], p[0]), max(c[0], p[0]) + 1):
                    rocks.add((j, c[1]))
    return rocks


input_data = get_input_data()


def solve_1() -> int:
    rocks: set(tuple(int, int)) = input_data.copy()

    max_rock_y = max(rocks, key=lambda x: x[1])[1]
    sands = 0
    cont = True
    while cont:
        sands += 1
        pos = [500, 0]
        while pos[1] <= max_rock_y:
            # check below
            down_pos = [pos[0], pos[1] + 1]
            if tuple(down_pos) not in rocks:
                pos = down_pos
                continue
            # check diag-left
            d_left = [pos[0] - 1, pos[1] + 1]
            if tuple(d_left) not in rocks:
                pos = d_left
                continue
            # check diag-right
            d_right = [pos[0] + 1, pos[1] + 1]
            if tuple(d_right) not in rocks:
                pos = d_right
                continue

            # not movement possible - rest
            # add to "rocks"
            rocks.add(tuple(pos))
            break
        else:
            # fallen to void
            cont = False

    return sands - 1


def solve_2() -> int:
    rocks: set(tuple(int, int)) = input_data.copy()

    max_rock_y = max(rocks, key=lambda x: x[1])[1]
    floor_y = max_rock_y + 2

    sands = 0
    while (500, 0) not in rocks:
        sands += 1
        pos = [500, 0]
        while True:
            # check below
            down_pos = [pos[0], pos[1] + 1]
            if tuple(down_pos) not in rocks and pos[1] + 1 < floor_y:
                pos = down_pos
                continue
            # check diag-left
            d_left = [pos[0] - 1, pos[1] + 1]
            if tuple(d_left) not in rocks and pos[1] + 1 < floor_y:
                pos = d_left
                continue
            # check diag-right
            d_right = [pos[0] + 1, pos[1] + 1]
            if tuple(d_right) not in rocks and pos[1] + 1 < floor_y:
                pos = d_right
                continue

            # not movement possible - rest
            # add to "rocks"
            rocks.add(tuple(pos))
            break

    return sands


def _print_grid(rocks: set(tuple(int, int)), sands: set(tuple(int, int))) -> None:
    grid = [['.' for _ in range(40)] for _ in range(13)]
    for x, y in rocks:
        grid[y][x - 480] = '#'
    for x, y in sands:
        grid[y][x - 480] = 'o'
    s = []
    for row in grid:
        s.append(''.join(row))
    print('\n'.join(s))


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
