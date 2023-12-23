from __future__ import annotations

import argparse
from typing import NamedTuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''
EXPECTED_1 = 33
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
        input_text = get_input_text(19)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')

    blueprints = []
    for line in input_text.splitlines():
        t = line.split(': ')[1].split('. ')
        ore = int(t[0].split(' ')[4])
        clay = int(t[1].split(' ')[4])
        obsidian = (int(t[2].split(' ')[4]), int(t[2].split(' ')[7]))
        geode = (int(t[3].split(' ')[4]), int(t[3].split(' ')[7]))
        blueprints.append([ore, clay, obsidian, geode])
    return blueprints


input_data = get_input_data()


class State(NamedTuple):
    minute: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    ore: int
    clay: int
    obsidian: int
    geode: int


def solve_1() -> int:
    state = State(1, 1, 0, 0, 0, 0, 0, 0, 0)
    todo = [state]
    while todo:
        el = todo.pop(0)
        if el.minute == 25:
            continue

        # try to build robots

    return


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
