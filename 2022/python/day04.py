from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED_1 = 2
EXPECTED_2 = 4

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
        input_text = get_input_text(4)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip()
    return [x.split(',') for x in input_text.split()]


input_data = get_input_data()


def solve_1() -> int:
    total_overlaps = 0
    for elf_1, elf_2 in input_data:
        s1, e1 = map(int, elf_1.split('-'))
        s2, e2 = map(int, elf_2.split('-'))
        if (s1 >= s2 and e1 <= e2) or (s2 >= s1 and e2 <= e1):
            total_overlaps += 1
    return total_overlaps


def solve_2() -> int:
    overlaps = 0
    for elf_1, elf_2 in input_data:
        e1 = list(map(int, elf_1.split('-')))
        e2 = list(map(int, elf_2.split('-')))
        s = sorted([e1, e2])
        overlaps += s[1][0] <= s[0][1]
    return overlaps


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
