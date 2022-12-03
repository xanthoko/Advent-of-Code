from __future__ import annotations

from typing import Optional

from utils import get_input_text

EXAMPLE_INPUT = '''\
'''
# EXPECTED_1 =
# EXPECTED_2 =


def get_input_data(example: Optional[bool] = False) -> None:
    if example:
        input_text = EXAMPLE_INPUT.strip()
    else:
        input_text = get_input_text(dayOfInput)
    # TODO: implement code here
    return


input_data = get_input_data(True)


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
