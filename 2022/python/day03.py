from __future__ import annotations

import argparse
from typing import Optional

from utils import get_input_text

EXAMPLE_INPUT = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
# EXPECTED_1 = 157
# EXPECTED_2 = 70

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
        input_text = get_input_text(3)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip()
    return input_text.split()


input_data = get_input_data()


def get_error(rucksack: str) -> str:
    h1, h2 = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
    return list(set(h1).intersection(set(h2)))[0]


def get_priority(error: str) -> int:
    if error.islower():
        return ord(error) - ord('a') + 1
    else:
        return ord(error) - ord('A') + 27


def solve_1() -> int:
    priorities = 0
    for rucksack in input_data:
        error = get_error(rucksack)
        priorities += get_priority(error)
    return priorities


def solve_2() -> int:
    priorities = 0
    for i in range(0, len(input_data), 3):
        s1 = set(input_data[i])
        s2 = set(input_data[i + 1])
        s3 = set(input_data[i + 2])
        badge = list(set.intersection(s1, s2, s3))[0]
        priorities += get_priority(badge)
    return priorities


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
