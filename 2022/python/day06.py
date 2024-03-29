from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
'''
EXPECTED_1 = 11
EXPECTED_2 = 26

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
        input_text = get_input_text(6)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return input_text


input_data = get_input_data()


def solve_1() -> int:
    s = input_data
    for i in range(4, len(s)):
        if len(set(s[i - 4:i])) == 4:
            return i


def solve_2() -> int:
    s = input_data
    for i in range(14, len(s)):
        if len(set(s[i - 14:i])) == 14:
            return i


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
