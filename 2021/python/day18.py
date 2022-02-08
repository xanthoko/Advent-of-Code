from math import ceil
from math import floor
from typing import List
from typing import Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''
# EXPECTED_1 = 4140
# EXPECTED_2 = 3993

RUN_MANUAL_TESTS = True


def get_input_data(example: bool = False) -> List[str]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(18)

    return input_text.strip().splitlines()


input_data = get_input_data()


def split_to_partitions(snail: str) -> List[str]:
    '''
    Let's say snail = [3,[34,5]]

    Simple parser: ['3', '[', ',', '[', '3', '4', ',', '5', ']']
    Partition parser: ['3', '[', ',', '[', '34', ',', '5', ']']
    '''
    partitioned_snail: List[str] = []
    ind = 0

    while ind < len(snail):
        char = snail[ind]

        if char in ['[', ']', ',']:
            partitioned_snail.append(char)
            ind += 1
        else:
            rolling_index = ind
            complete_str_number = ''  # whole number
            while char not in ['[', ']', ','] and rolling_index < len(snail) - 1:
                complete_str_number += char
                rolling_index += 1
                char = snail[rolling_index]

            partitioned_snail.append(complete_str_number)
            ind += (rolling_index - ind)

    return partitioned_snail


def explode(snail: str) -> Tuple[str, bool]:
    snail = snail.replace(' ', '')  # spaces are problems
    exploded_snail = split_to_partitions(snail)

    sind = 0  # snail index
    exploded = False
    open_par_counter = 0  # open parentheses counter

    while sind < len(exploded_snail):
        char: str = exploded_snail[sind]
        if char == '[':
            open_par_counter += 1
            if open_par_counter == 5:
                exploded = True
                p1 = int(exploded_snail[sind + 1])
                p2 = int(exploded_snail[sind + 3])

                # search for the first number to the left
                p1_ind = sind - 1
                while p1_ind >= 0:
                    try:
                        number = int(exploded_snail[p1_ind]) + p1
                        # replace number
                        exploded_snail[p1_ind] = str(number)
                        break
                    except ValueError:
                        p1_ind -= 1

                # search for the first number to the right
                p2_ind = sind + 4  # start from the end of the exploding pair
                while p2_ind < len(exploded_snail):
                    try:
                        new_n = int(exploded_snail[p2_ind]) + p2
                        # replace number
                        exploded_snail[p2_ind] = str(new_n)
                        break
                    except ValueError:
                        p2_ind += 1

                # replace exploded pair with 0
                exploded_snail[sind:sind + 5] = '0'
                break
        elif char == ']':
            open_par_counter -= 1

        sind += 1

    return ''.join(exploded_snail), exploded


def split(snail: str) -> Tuple[str, bool]:
    sind = 0  # snail index
    splitted = False
    splitted_snail = split_to_partitions(snail)

    while sind < len(splitted_snail) - 1:
        try:
            number = int(splitted_snail[sind])
            if number > 9:
                splitted = True
                p1 = floor(number / 2)
                p2 = ceil(number / 2)
                splitted_snail[sind] = f'[{p1},{p2}]'
                break
            else:
                sind += 1
        except ValueError:
            sind += 1

    return ''.join(splitted_snail), splitted


def addition(snail1: str, snail2: str) -> str:
    snail = f'[{snail1},{snail2}]'
    action_taken = True

    while action_taken:
        snail, exploded = explode(snail)
        if exploded:
            continue

        snail, splitted = split(snail)
        action_taken = exploded or splitted

    return snail


def get_magnitude(snail: str) -> int:
    inside: str = snail[1:-1]
    if '[' not in inside:
        p1, p2 = inside.split(',')
        return int(p1) * 3 + int(p2) * 2

    open_par_counter = 0
    parts: List[int] = []
    temp_str = ''

    for ch in inside:
        temp_str += ch
        if ch == '[':
            open_par_counter += 1
        elif ch == ']':
            open_par_counter -= 1
        if open_par_counter == 0:  # balance achieved
            if ch != ',':
                if '[' in temp_str:
                    parts.append(get_magnitude(temp_str))
                else:
                    parts.append(int(temp_str))
            temp_str = ''

    return parts[0] * 3 + parts[1] * 2


def solve_1() -> int:
    res = input_data[0]
    ind = 0
    while ind < len(input_data) - 1:
        res = addition(res, input_data[ind + 1])
        ind += 1

    return get_magnitude(res)


def solve_2() -> int:
    max_mag = -1
    for i in range(len(input_data) - 1):
        for j in range(i + 1, len(input_data)):
            added_snail = addition(input_data[i], input_data[j])
            magnitude = get_magnitude(added_snail)
            if magnitude > max_mag:
                max_mag = magnitude

            reverse_added_snail = addition(input_data[j], input_data[i])
            magnitude = get_magnitude(reverse_added_snail)
            if magnitude > max_mag:
                max_mag = magnitude

    return max_mag


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':

    if RUN_MANUAL_TESTS:
        # explition tests
        assert explode('[[[[[9,8],1],2],3],4]')[0] == '[[[[0,9],2],3],4]'
        assert explode('[7,[6,[5,[4,[3,2]]]]]')[0] == '[7,[6,[5,[7,0]]]]'
        assert explode('[[6,[5,[4,[3, 2]]]],1]')[0] == '[[6,[5,[7,0]]],3]'
        assert explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'
                       )[0] == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
        assert explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
                       )[0] == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'
        print('[TEST] Explode tests PASSED')

        # split tests
        assert split('[[[[0,7],4],[15,[0,13]]],[1,1]]'
                     )[0] == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
        assert split('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
                     )[0] == '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'
        print('[TEST] Split tests PASSED')

        # magnitude tests
        assert get_magnitude('[[9,1],[1,9]]') == 129
        assert get_magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384
        assert get_magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445
        assert get_magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791
        assert get_magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137
        assert get_magnitude(
            '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488
        print('[TEST] Magnitude tests PASSED')

        # addition tests
        assert addition('[[[[4,3],4],4],[7,[[8,4],9]]]',
                        '[1,1]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
        assert addition(
            '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'
        ) == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'
        print('[TEST] Addition tests PASSED')

    solve()
