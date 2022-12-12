from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED_1 = 13140
EXPECTED_2 = None

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
        input_text = get_input_text(10)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    return input_text.splitlines()


input_data = get_input_data()


def solve_1() -> int:
    cycles = 1
    x = 1
    res = 0
    for cmd in input_data:
        if cycles in [20, 60, 100, 140, 180, 220]:
            res += cycles * x
        inst, *val = cmd.split(' ')
        if inst == 'noop':
            cycles += 1
        elif inst == 'addx':
            cycles += 1
            if cycles in [20, 60, 100, 140, 180, 220]:
                res += cycles * x
            cycles += 1
            x += int(val[0])
    return res


def solve_2() -> int:
    cycles = 0
    rows: list[str] = ['' for _ in range(6)]
    sprite_pos = 1  # 0 indexed

    for i, cmd in enumerate(input_data):
        row, pos = divmod(cycles, 40)  # 0 indexed
        # draw pixel in position row, pos
        # check if drawing is in sprite
        if pos in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            rows[row] += '#'
        else:
            rows[row] += ' '

        cycles += 1
        splt = cmd.split(' ')

        if splt[0] == 'addx':
            row, pos = divmod(cycles, 40)  # 0 indexed
            if pos in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
                rows[row] += '#'
            else:
                rows[row] += ' '

            cycles += 1
            sprite_pos = (sprite_pos + int(splt[1])) % 40

    return '\n'.join(rows)


def _validate(expected, actual):
    if not is_production:
        error_msg = f'\033[41mExpected: {expected}. Got: {actual}\033[m'
        assert actual == expected, error_msg


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')
    _validate(EXPECTED_1, part_1)

    part_2 = solve_2()
    print(f'Part 2:\n{part_2}')
    v = """\
##  ##  ##  ##  ##  ##  ##  ##  ##  ##
###   ###   ###   ###   ###   ###   ###
####    ####    ####    ####    ####
#####     #####     #####     #####
######      ######      ######      ####
#######       #######       #######     """
    if not is_production:
        assert part_2 == v


if __name__ == '__main__':
    solve()
