from __future__ import annotations

import argparse
from typing import Optional

from utils import get_input_text

EXAMPLE_INPUT = '''\
A Y
B X
C Z
'''
# EXPECTED_1 = 15
# EXPECTED_2 = 12

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
        input_text = get_input_text(2)
    else:
        input_text = EXAMPLE_INPUT.strip()
    return input_text.strip().split('\n')


input_data = get_input_data()

shape_score = {'X': 1, 'Y': 2, 'Z': 3}
pvp = {
    'A': ['Y', 'Z', 'X'],
    'B': ['Z', 'X', 'Y'],
    'C': ['X', 'Y', 'Z'],
}


def round_score(s1: str, s2: str) -> int:
    if s2 == 'X':
        if s1 == 'A':
            return 3
        elif s1 == 'B':
            return 0
        else:
            return 6
    elif s2 == 'Y':
        if s1 == 'A':
            return 6
        elif s1 == 'B':
            return 3
        else:
            return 0
    elif s2 == 'Z':
        if s1 == 'A':
            return 0
        elif s1 == 'B':
            return 6
        else:
            return 3


def solve_1() -> int:
    total_score = 0
    for round in input_data:
        enemy, me = round.split()
        total_score += (round_score(enemy, me) + shape_score[me])
    return total_score


def solve_2() -> int:
    total_score = 0
    for round in input_data:
        enemy, outcome = round.split()
        if outcome == 'X':
            total_score += (0 + shape_score[pvp[enemy][1]])
        elif outcome == 'Y':
            total_score += (3 + shape_score[pvp[enemy][2]])
        else:
            total_score += (6 + shape_score[pvp[enemy][0]])
    return total_score


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
