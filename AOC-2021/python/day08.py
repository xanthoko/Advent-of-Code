from typing import List
from collections import Counter

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(8)
    splited_str_input_list = input_text.split('\n')
    return [x.split(' | ') for x in splited_str_input_list]


def get_unique_digits(lines: List[List[str]]) -> int:
    total_counter = Counter()
    for _, output in lines:
        total_counter.update(Counter([len(x) for x in output.split()]))
    return total_counter[2] + total_counter[3] + total_counter[4] + total_counter[7]


def get_sum_of_output(lines: List[List[str]]) -> int:
    determined_lengths = {2: '1', 3: '7', 4: '4', 7: '8'}

    total_output = 0
    for pattern, output in lines:
        splitted_output = output.split()

        splitted_pattern = sorted(pattern.split(), key=lambda x: len(x))
        right_segments = [splitted_pattern[0][0], splitted_pattern[0][1]]
        # segments of four that are not in segment 1
        of_four_segments = [
            x for x in splitted_pattern[2] if x not in right_segments
        ]

        translated_output = ''
        for mixed in splitted_output:
            if len(mixed) in determined_lengths:
                translated_output += determined_lengths[len(mixed)]
            else:
                if len(mixed) == 6:  # either a 6, 9 or 0
                    # if all the segments of 4 are in the mixed its a 9
                    if all([x in mixed for x in splitted_pattern[2]]):
                        translated_output += '9'
                    elif all([x in mixed for x in right_segments]):
                        translated_output += '0'
                    else:
                        translated_output += '6'
                elif len(mixed) == 5:
                    if all([x in mixed for x in right_segments]):
                        translated_output += '3'
                    elif all([x in mixed for x in of_four_segments]):
                        translated_output += '5'
                    else:
                        translated_output += '2'
        total_output += int(translated_output)
    return total_output


def solve():
    lines = get_input_list()

    # PART 1
    easy_digits = get_unique_digits(lines)
    print(f'{easy_digits} unique digits')

    # PART 2
    total_output = get_sum_of_output(lines)
    print(f'Total output: {total_output}')


if __name__ == '__main__':
    solve()
