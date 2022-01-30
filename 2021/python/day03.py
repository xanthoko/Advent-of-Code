from typing import List

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(3)
    splited_str_input_list = input_text.strip().split('\n')
    return splited_str_input_list


def get_power_consumption(binaries: List[str]) -> int:
    ones_counter = [0] * len(
        binaries[0])  # counts the number of '1' in each position
    for binary in binaries:
        for i, el in enumerate(binary):
            ones_counter[i] += int(el)

    gamma_rate_bit_list = list(
        map(lambda x: str(int(x > (len(binaries) // 2))),
            ones_counter))  # ['0', '1', '0', ...]
    gamma_rate_bin = ''.join(gamma_rate_bit_list)  # '010...'
    gamma_rate = int(gamma_rate_bin, 2)

    epsilon_rate_bit_list = list(
        map(lambda x: str(int(x <= (len(binaries) // 2))), ones_counter))
    epsilon_rate_bin = ''.join(epsilon_rate_bit_list)
    epsilon_rate = int(epsilon_rate_bin, 2)

    return gamma_rate * epsilon_rate


def get_life_support_rating(binaries: List[str]) -> int:
    oxygen_generator_rating = _apply_bit_creteria(binaries.copy(), '1', '0')
    co2_scrubber_rating = _apply_bit_creteria(binaries.copy(), '0', '1')
    return oxygen_generator_rating * co2_scrubber_rating


def _apply_bit_creteria(remains: List[str], main: str, secondary: str):
    index = 0

    while len(remains) > 1 and index < len(remains[0]):
        one_counter = sum([int(x[index]) for x in remains])
        determinant = main if one_counter >= len(remains) / 2 else secondary

        # remove numbers
        remains = [x for x in remains if x[index] == determinant]
        index += 1

    return int(remains[0], 2)


def solve():
    binaries = get_input_list()

    # PART 1
    power_consumption = get_power_consumption(binaries)
    print(f'Power consumption is {power_consumption}')

    # PART 2
    life_support_rating = get_life_support_rating(binaries)
    print(f'Life support rating is {life_support_rating}')


if __name__ == '__main__':
    solve()
