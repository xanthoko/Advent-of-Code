import itertools
from typing import List
from typing import Tuple
'''
2 Types of digits
Type 1: z *= 26  (makes z 26 times bigger)
Type 2: z ~= z or z /= 26  (leaves z untouched or makes z 26 times smaller)
The condition for type 2 digits to make z smaller is w = z % 26 - a
'''

incs = [14, 2, 1, 13, 5, None, None, 9, None, 13, None, None, None, None]
decs = [None, None, None, None, None, 12, 12, None, 7, None, 8, 5, 10, 7]


def _are_digits_valid(digits: Tuple[int]) -> List[int]:
    z = 0
    digit_ind = 0
    res = [0] * 14

    for i in range(14):
        inc, dec = incs[i], decs[i]

        if inc == None:
            assert dec is not None  # to satisfy mypy
            res[i] = z % 26 - dec
            z //= 26
            if not (1 <= res[i] <= 9):
                return []
        else:
            assert inc is not None  # to satisfy mypy
            digit = digits[digit_ind]
            z = 26 * z + digit + inc
            res[i] = digit
            digit_ind += 1
    return res


def find_valid_digits(digits_space: itertools.product) -> str:
    for digits in digits_space:
        ret = _are_digits_valid(digits)
        if ret:
            return ''.join(str(x) for x in ret)
    return 'no valid digits found'


def solve() -> None:
    digits_space_1 = itertools.product(range(9, 0, -1), repeat=7)
    part_1 = find_valid_digits(digits_space_1)
    print(f'Part 1: {part_1}')

    digits_space_2 = itertools.product(range(1, 10), repeat=7)
    part_2 = find_valid_digits(digits_space_2)
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
