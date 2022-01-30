from typing import List

from utils import get_input_text


def get_input_list() -> List[int]:
    input_text = get_input_text(1)
    splited_str_input_list = input_text.strip().split('\n')
    input_list = list(map(int, splited_str_input_list))
    return input_list


def get_increases(input_list: List[int]) -> int:
    increases_counter = 0
    for i in range(1, len(input_list)):
        increases_counter += input_list[i] > input_list[i - 1]
    return increases_counter


def get_windowed_increases(input_list: List[int]) -> int:
    increases_counter = 0
    for i in range(3, len(input_list)):
        window_1_sum = _get_window_sum(input_list, i - 1)
        window_2_sum = _get_window_sum(input_list, i)
        increases_counter += window_2_sum > window_1_sum
    return increases_counter


def _get_window_sum(input_list: List[int], index: int) -> int:
    return input_list[index] + input_list[index - 1] + input_list[index - 2]


def solve():
    input_list = get_input_list()

    # PART 1
    increases = get_increases(input_list)
    print(f'{increases} increases found')

    # PART 2
    windowed_increases = get_windowed_increases(input_list)
    print(f'{windowed_increases} windowed increases found')


if __name__ == '__main__':
    solve()
