from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''
# EXPECTED_1 = 24000
# EXPECTED_2 = 45000


def get_input_data(example: Optional[bool] = False) -> list[str]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(1)

    return input_text.split('\n\n')


input_data = get_input_data()


def solve_1() -> int:
    calories = []
    for deer_food in input_data:
        calories.append(sum(map(int, deer_food.split('\n'))))
    return max(calories)


def solve_2() -> int:
    calories = []
    for deer_food in input_data:
        calories.append(sum(map(int, deer_food.split('\n'))))
    calories.sort()
    return calories[-1] + calories[-2] + calories[-3]


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
