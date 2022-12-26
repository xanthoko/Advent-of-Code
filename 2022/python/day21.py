from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
EXPECTED_1 = 152
EXPECTED_2 = 301

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
        input_text = get_input_text(21)
    else:
        input_text = EXAMPLE_INPUT
    input_text = input_text.strip('\n')
    ret = {}
    for line in input_text.splitlines():
        a, b = line.split(': ')
        try:
            ret[a] = int(b)
        except ValueError:
            ret[a] = b.split(' ')
    return ret


input_data = get_input_data()


def solve_1(name: str = 'root') -> int:
    b = input_data[name]
    if isinstance(b, int):
        return b

    assert len(b) == 3
    op1, sign, op2 = b
    if sign == '+':
        return solve_1(op1) + solve_1(op2)
    elif sign == '-':
        return solve_1(op1) - solve_1(op2)
    elif sign == '*':
        return solve_1(op1) * solve_1(op2)
    elif sign == '/':
        return solve_1(op1) // solve_1(op2)
    else:
        raise NotImplementedError(sign)


def helper(name: str) -> int:
    if name == 'humn':
        return
    b = input_data[name]
    if isinstance(b, int):
        return b

    assert len(b) == 3
    op1, sign, op2 = b
    e1 = helper(op1)
    e2 = helper(op2)
    if e1 is None or e2 is None:
        return
    if sign == '+':
        return e1 + e2
    elif sign == '-':
        return e1 - e2
    elif sign == '*':
        return e1 * e2
    elif sign == '/':
        return e1 // e2
    else:
        raise NotImplementedError(sign)


def find_num(name: str, target: int = None) -> int:
    if name == 'humn':
        return target

    s1, sign, s2 = input_data[name]
    h1 = helper(s1)
    h2 = helper(s2)
    if h1 is None:  # humn in the first side
        if sign == '+':
            return find_num(s1, target - h2)
        elif sign == '-':
            return find_num(s1, target + h2)
        elif sign == '*':
            return find_num(s1, target // h2)
        elif sign == '/':
            return find_num(s1, target * h2)
        elif sign == '=':
            return find_num(s1, h2)
    else:
        if sign == '+':
            return find_num(s2, target - h1)
        elif sign == '-':
            return find_num(s2, h1 - target)
        elif sign == '*':
            return find_num(s2, target // h1)
        elif sign == '/':
            return find_num(s2, target * h1)
        elif sign == '=':
            return find_num(s2, h1)


def solve_2() -> int:
    input_data['root'][1] = '='
    return find_num('root')


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
