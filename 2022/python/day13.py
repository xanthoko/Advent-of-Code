from __future__ import annotations

import argparse
import functools
import json

from utils import get_input_text

EXAMPLE_INPUT = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED_1 = 13
EXPECTED_2 = 140

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
        input_text = get_input_text(13)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return input_text.split('\n\n')


input_data = get_input_data()


def compare(v1: list[int], v2: list[int]) -> bool:
    if isinstance(v1, int) and isinstance(v2, int):
        if v1 < v2:
            return 1
        elif v1 > v2:
            return -1
        else:
            return 0

    if not type(v1) == list:
        v1 = [v1]
    if not type(v2) == list:
        v2 = [v2]

    ind1, ind2 = 0, 0
    while ind1 < len(v1) and ind2 < len(v2):
        x = compare(v1[ind1], v2[ind2])
        if x == 1:
            return 1
        if x == -1:
            return -1

        ind1 += 1
        ind2 += 1

    if ind1 == len(v1) and ind2 == len(v2):
        return 0
    if ind1 == len(v1):
        return 1
    elif ind2 == len(v2):
        return -1

    return 0


def solve_1() -> int:
    res = 0
    for i, pair in enumerate(input_data):
        val1_s, val2_s = pair.splitlines()
        val1: list[int] = json.loads(val1_s)
        val2: list[int] = json.loads(val2_s)
        if compare(val1, val2) == 1:
            res += i + 1
    return res


def solve_2() -> int:
    packets = []
    for pair in input_data:
        ps = map(json.loads, pair.splitlines())
        packets += ps
    # add divider packets
    packets += [[[2]], [[6]]]

    # sort packets to correctness
    packets.sort(key=functools.cmp_to_key(compare), reverse=True)

    # find divider
    ind_1 = packets.index([[2]])
    ind_2 = packets.index([[6]])
    return (ind_1 + 1) * (ind_2 + 1)


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
