from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
30373
25512
65332
33549
35390
'''
EXPECTED_1 = 21
EXPECTED_2 = 8

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
        input_text = get_input_text(8)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return [[int(x) for x in row] for row in input_text.splitlines()]


input_data = get_input_data()


def solve_1() -> int:
    grid = input_data
    rows, cols = len(grid), len(grid[0])
    visible_trees = cols * 2 + (rows - 2) * 2
    seen: set(tuple(int, int)) = set()

    for r in range(1, rows - 1):
        # left
        cur_max = grid[r][0]
        for c in range(1, cols - 1):
            if grid[r][c] > cur_max:
                cur_max = grid[r][c]
                if (r, c) not in seen:
                    visible_trees += 1
                    seen.add((r, c))

        # right
        cur_max = grid[r][-1]
        for c in range(cols - 2, 0, -1):
            if grid[r][c] > cur_max:
                cur_max = grid[r][c]
                if (r, c) not in seen:
                    visible_trees += 1
                    seen.add((r, c))

    for c in range(1, cols - 1):
        # top
        cur_max = grid[0][c]
        for r in range(1, rows - 1):

            if grid[r][c] > cur_max:
                cur_max = grid[r][c]
                if (r, c) not in seen:
                    visible_trees += 1
                    seen.add((r, c))

        # bot
        cur_max = grid[-1][c]
        for r in range(rows - 2, 0, -1):
            if grid[r][c] > cur_max:
                cur_max = grid[r][c]
                if (r, c) not in seen:
                    visible_trees += 1
                    seen.add((r, c))

    return visible_trees


def solve_2() -> int:
    grid = input_data
    rows, cols = len(grid), len(grid[0])
    scores = [[1 for _ in range(rows)] for _ in range(cols)]

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            el = grid[r][c]
            # look right
            for k in range(c + 1, cols):
                if el <= grid[r][k]:
                    break
            scores[r][c] *= k - c

            # look left
            for k in range(c - 1, -1, -1):
                if el <= grid[r][k]:
                    break
            scores[r][c] *= c - k

    for c in range(1, cols - 1):
        for r in range(1, rows - 1):
            el = grid[r][c]
            # look down
            for k in range(r + 1, rows):
                if el <= grid[k][c]:
                    break
            scores[r][c] *= k - r

            # look up
            for k in range(r - 1, -1, -1):
                if el <= grid[k][c]:
                    break
            scores[r][c] *= r - k

    return max(max(row) for row in scores)


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
