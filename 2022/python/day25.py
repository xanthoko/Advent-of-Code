from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''
EXPECTED_1 = '2=-1=0'
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
        input_text = get_input_text(25)
    else:
        input_text = EXAMPLE_INPUT
    input_text = input_text.strip('\n')
    return input_text.splitlines()


input_data = get_input_data()


def solve_1() -> int:
    sum = 0
    for line in input_data:
        decimal_value = 0
        for i, c in enumerate(line):
            current_c_value = 5**(len(line) - i - 1)
            if c == '-':
                decimal_value -= current_c_value
            elif c == '=':
                decimal_value -= 2 * current_c_value
            else:
                decimal_value += int(c) * current_c_value

        sum += decimal_value
    return _convert_decimal_to_snafu(sum)


'''
4082
4    * 1000   + 0 * 100    + 8    * 10   + 2 * 1
4    * (2=00) + 0 * (1-00) + 8    * (20) + 2 * 1
(1-) * (2=00) + 0 * (1-00) + (2=) * (20) + 2 * 1

(num_of_digits = 6)
max_value_at_6 = 2 * 5**(5) = 6250 (6250/2 = 3125)
4000 -> XXXXXX | 112000
num_of_digits = math.ceil(math.log(dec/2, 5) + 1)
max_value_at_i = 2 * 5**(i-1)

1
5
25
125
625
3125
'''


def _convert_decimal_to_snafu(decimal_value: int) -> str:
    return ''


def _validate(expected, actual):
    if not is_production:
        error_msg = f'\033[41mExpected: {expected}. Got: {actual}\033[m'
        assert actual == expected, error_msg


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')
    _validate(EXPECTED_1, part_1)


if __name__ == '__main__':
    solve()
