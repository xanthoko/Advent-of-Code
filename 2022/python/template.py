from __future__ import annotations

import argparse
from typing import Optional

from utils import get_input_text

EXAMPLE_INPUT = '''\
'''
# EXPECTED_1 =
# EXPECTED_2 =

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
        input_text = get_input_text(dayOfInput)
    else:
        input_text = EXAMPLE_INPUT.strip()
    # TODO: implement code here
    return


input_data = get_input_data()


def solve_1() -> int:
    # TODO: implement solution here
    pass


def solve_2() -> int:
    # TODO: implement solution here
    pass


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
