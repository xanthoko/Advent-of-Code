from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED_1 = 88
EXPECTED_2 = 36

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
        input_text = get_input_text(9)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return input_text.splitlines()


input_data = get_input_data()


def _move_head(head: list[int], direction: str) -> None:
    if direction == 'R':
        head[1] += 1
    elif direction == 'L':
        head[1] -= 1
    elif direction == 'U':
        head[0] -= 1
    elif direction == 'D':
        head[0] += 1


def _check_if_knot_must_move(head: list[int], tail: list[int]) -> bool:
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            dt = [tail[0] + dr, tail[1] + dc]
            if dt == head:
                return False
    return True


def _move_tail(head: list[int], tail: list[int]) -> None:
    if head[0] == tail[0]:  # same row
        if head[1] < tail[1]:
            tail[1] -= 1
        else:
            tail[1] += 1
    elif head[1] == tail[1]:  # same col
        if head[0] < tail[0]:
            tail[0] -= 1
        else:
            tail[0] += 1
    else:
        if head[1] < tail[1]:
            tail[1] -= 1
        else:
            tail[1] += 1
        if head[0] < tail[0]:
            tail[0] -= 1
        else:
            tail[0] += 1


def solve_1() -> int:
    head, tail = [0, 0], [0, 0]
    visited: set(tuple(int, int)) = set()

    for cmd in input_data:
        direction, val = cmd.split(' ')
        for _ in range(int(val)):
            _move_head(head, direction)

            if _check_if_knot_must_move(head, tail):
                _move_tail(head, tail)
            visited.add(tuple(tail))

    return len(visited)


def solve_2() -> int:
    knots = [[0, 0] for _ in range(10)]
    visited: set(tuple(int, int)) = set()

    for cmd in input_data:
        direction, val = cmd.split(' ')
        for _ in range(int(val)):
            _move_head(knots[0], direction)

            for i in range(1, 10):
                if _check_if_knot_must_move(knots[i - 1], knots[i]):
                    _move_tail(knots[i - 1], knots[i])
            visited.add(tuple(knots[-1]))
    return len(visited)


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
