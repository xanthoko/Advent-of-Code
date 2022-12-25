from __future__ import annotations

import argparse
import itertools
import json

from utils import get_input_text

EXAMPLE_INPUT = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED_1 = 3068
EXPECTED_2 = 1514285714288

ROCKS = '''\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''.split('\n\n')
ROCKS = [
    '[[0, 3], [0, 4], [0, 5], [0, 6]]',
    '[[0, 4], [1, 3], [1, 4], [1, 5], [2, 4]]',
    '[[0, 3], [0, 4], [0, 5], [1, 5], [2, 5]]',
    '[[0, 3], [1, 3], [2, 3], [3, 3]]',
    '[[0, 3], [0, 4], [1, 3], [1, 4]]',
]  # shifted right by 3 units (starting position)

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
        input_text = get_input_text(17)
    else:
        input_text = EXAMPLE_INPUT
    input_text = input_text.strip('\n')
    return input_text


input_data = get_input_data()


def push_rock(rock: list[list[int]], gas: str,
              existing_rocks: set(tuple(int, int))) -> None:
    left_wall_c = 0
    right_wall_c = 8
    if gas == '>':
        rightest_part = max(x[1] for x in rock)
        if right_wall_c - rightest_part > 1 and not any(
            (x[0], x[1] + 1) in existing_rocks for x in rock):
            # move
            for i in range(len(rock)):
                rock[i][1] += 1
    elif gas == '<':
        leftest_part = min(x[1] for x in rock)
        if leftest_part - left_wall_c > 1 and not any(
            (x[0], x[1] - 1) in existing_rocks for x in rock):
            # move
            for i in range(len(rock)):
                rock[i][1] -= 1


def _print_rocks(rocks: set[tuple[int, int]],
                 falling: list[list[int]] = []) -> None:
    tallest_point = max(x[0] for x in rocks)
    piv = 25
    terrain = [['|', '.', '.', '.', '.', '.', '.', '.', '|'] for _ in range(piv)]
    for r in rocks:
        terrain[piv - 1 - r[0]][r[1]] = '#'
    for f in falling:
        terrain[piv - 1 - f[0]][f[1]] = '@'
    t = []
    for row in terrain:
        t.append(''.join(row))
        # print(t)
    print('\n'.join(t))
    print()


def solve_1() -> int:
    gas_iter = itertools.cycle(input_data)
    rock_iter = itertools.cycle(ROCKS)
    existing_rocks: set[tuple[int, int]] = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                                            (0, 6), (0, 7)}
    for _ in range(2022):
        rock: list[list[int]] = json.loads(next(rock_iter))
        # intialize rock position
        tallest_pos = max(x[0] for x in existing_rocks)
        for i in range(len(rock)):
            rock[i][0] += tallest_pos + 4

        while True:  # while rock falling
            gas = next(gas_iter)
            # pushed by gas
            push_rock(rock, gas, existing_rocks)
            # fall
            # check if any of the rocks coords will touch any
            new_coords: list[list[int]] = [[r[0] - 1, r[1]] for r in rock]
            for r in rock:
                new_coords.append([r[0] - 1, r[1]])
            # existing rock
            if any(tuple(x) in existing_rocks for x in new_coords):
                existing_rocks.update({tuple(x) for x in rock})
                break
            else:
                rock = new_coords
    return max(x[0] for x in existing_rocks)


def solve_2() -> int:
    # --- find pattern ---
    gas_iter = itertools.cycle(enumerate(input_data))
    rock_iter = itertools.cycle(enumerate(ROCKS))
    existing_rocks: set[tuple[int, int]] = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                                            (0, 6), (0, 7)}

    patterns = []
    skylines = []
    ind = 0
    pattern_size, pattern_height = None, None
    while ind < 1000000000000:
        rind, rock = next(rock_iter)
        rock = json.loads(rock)
        # intialize rock position
        tallest_pos = max(x[0] for x in existing_rocks)
        for i in range(len(rock)):
            rock[i][0] += tallest_pos + 4

        gind, gas = next(gas_iter)
        # skyline
        skyline = [
            max(x[0] for x in existing_rocks if x[1] == i) for i in range(1, 8)
        ]
        skylines.append(skyline)
        # normalize skyline
        normed = [skyline[i] - min(skyline) for i in range(7)]

        pattern = (tuple(normed), gind, rind)
        if pattern in patterns:
            current, prev = ind, patterns.index(pattern)
            pattern_size = current - prev
            pattern_height = skylines[current][0] - skylines[prev][0]
            break

        patterns.append(pattern)

        while True:  # while rock falling
            # pushed by gas
            push_rock(rock, gas, existing_rocks)
            # fall
            # check if any of the rocks coords will touch any
            new_coords: list[list[int]] = [[r[0] - 1, r[1]] for r in rock]
            # existing rock
            if any(tuple(x) in existing_rocks for x in new_coords):
                existing_rocks.update({tuple(x) for x in rock})
                break
            else:
                rock = new_coords
            gind, gas = next(gas_iter)
        ind += 1

    goal = 1000000000000
    distance = goal - current
    fitting = distance // pattern_size
    final_station = current + pattern_size * fitting
    sk_fs = [skylines[current][i] + pattern_height * fitting for i in range(7)]
    remainder = goal - final_station
    gained = [skylines[prev + remainder][i] - skylines[prev][i] for i in range(7)]
    return max(sk_fs[i] + gained[i] for i in range(7))


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
