from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED_1 = 10605
EXPECTED_2 = 2713310158

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
        input_text = get_input_text(11)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return input_text.split('\n\n')


input_data = get_input_data()


def solve_1() -> int:
    inspections: list[int] = [0] * len(input_data)
    items: list[list[int]] = []
    functions: list[callable] = [
        lambda x: x * 19,
        lambda x: x + 6,
        lambda x: x * x,
        lambda x: x + 3,
    ]
    conditions: list[callable] = [
        lambda x: x % 23 == 0,
        lambda x: x % 19 == 0,
        lambda x: x % 13 == 0,
        lambda x: x % 17 == 0,
    ]
    actions = [
        (2, 3),
        (2, 0),
        (1, 3),
        (0, 1),
    ]
    # functions: list[callable] = [
    #     lambda x: x * 17,
    #     lambda x: x + 5,
    #     lambda x: x + 8,
    #     lambda x: x + 1,
    #     lambda x: x + 4,
    #     lambda x: x * 7,
    #     lambda x: x + 6,
    #     lambda x: x * x,
    # ]
    # conditions: list[callable] = [
    #     lambda x: x % 19 == 0,
    #     lambda x: x % 13 == 0,
    #     lambda x: x % 5 == 0,
    #     lambda x: x % 7 == 0,
    #     lambda x: x % 17 == 0,
    #     lambda x: x % 2 == 0,
    #     lambda x: x % 3 == 0,
    #     lambda x: x % 11 == 0,
    # ]
    # actions = [
    #     (5, 3),
    #     (7, 6),
    #     (3, 0),
    #     (4, 5),
    #     (1, 6),
    #     (1, 4),
    #     (7, 2),
    #     (0, 2),
    # ]

    for monkey in input_data:
        l = monkey.splitlines()
        items.append(list(map(int, l[1].split(': ')[1].split(', '))))

    for _ in range(20):
        for m in range(len(input_data)):
            for i in range(len(items[m])):
                new_worry_level = functions[m](items[m][i]) // 3
                if conditions[m](new_worry_level):
                    # move to actions[m][0]
                    dst = actions[m][0]
                    items[dst].append(new_worry_level)
                else:
                    # move to actions[m][1]
                    dst = actions[m][1]
                    items[dst].append(new_worry_level)

                # update inspections
                inspections[m] += 1
            # clear monkey items
            items[m] = []

    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def solve_2() -> int:
    inspections: list[int] = [0] * len(input_data)
    items: list[list[int]] = []
    functions: list[callable] = [
        lambda x: x * 19,
        lambda x: x + 6,
        lambda x: x * x,
        lambda x: x + 3,
    ]
    conditions: list[callable] = [
        lambda x: x % 23 == 0,
        lambda x: x % 19 == 0,
        lambda x: x % 13 == 0,
        lambda x: x % 17 == 0,
    ]
    actions = [
        (2, 3),
        (2, 0),
        (1, 3),
        (0, 1),
    ]
    # functions: list[callable] = [
    #     lambda x: x * 17,
    #     lambda x: x + 5,
    #     lambda x: x + 8,
    #     lambda x: x + 1,
    #     lambda x: x + 4,
    #     lambda x: x * 7,
    #     lambda x: x + 6,
    #     lambda x: x * x,
    # ]
    # conditions: list[callable] = [
    #     lambda x: x % 19 == 0,
    #     lambda x: x % 13 == 0,
    #     lambda x: x % 5 == 0,
    #     lambda x: x % 7 == 0,
    #     lambda x: x % 17 == 0,
    #     lambda x: x % 2 == 0,
    #     lambda x: x % 3 == 0,
    #     lambda x: x % 11 == 0,
    # ]
    # actions = [
    #     (5, 3),
    #     (7, 6),
    #     (3, 0),
    #     (4, 5),
    #     (1, 6),
    #     (1, 4),
    #     (7, 2),
    #     (0, 2),
    # ]

    for monkey in input_data:
        l = monkey.splitlines()
        items.append(list(map(int, l[1].split(': ')[1].split(', '))))

    for _ in range(10000):
        if _ % 20 == 0:
            print(inspections)
        for m in range(len(input_data)):
            for i in range(len(items[m])):
                new_worry_level = functions[m](items[m][i])
                # new_worry_level = items[m][i]
                if conditions[m](new_worry_level):
                    # move to actions[m][0]
                    dst = actions[m][0]
                    items[dst].append(new_worry_level)
                else:
                    # move to actions[m][1]
                    dst = actions[m][1]
                    items[dst].append(new_worry_level)

            # update inspections
            inspections[m] += len(items[m])
            # clear monkey items
            items[m] = []

    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


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
