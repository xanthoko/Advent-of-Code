from typing import List

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(7)
    splited_str_input_list = list(map(int, input_text.split(',')))
    return splited_str_input_list


def get_fuel_spent(crab_positions: List[int], _fuel_func) -> int:
    return min([
        _fuel_func(crab_positions, i) for i in range(min(crab_positions),
                                                     max(crab_positions) + 1)
    ])


def _calculate_liner_fuel(crab_positions: List[int], i: int) -> int:
    return sum([abs(x - i) for x in crab_positions])


def _calculate_expo_fuel(crab_positions: List[int], i: int) -> int:
    # Sum n, n=1 to x   =   (x^2 + x) / 2
    return sum([(abs(x - i)**2 + abs(x - i)) // 2 for x in crab_positions])


def solve():
    positions = get_input_list()

    # PART 1
    fuel_spent_1 = get_fuel_spent(positions, _calculate_liner_fuel)
    print(f'{fuel_spent_1} fuel spent')

    # PART 2
    fuel_spent_2 = get_fuel_spent(positions, _calculate_expo_fuel)
    print(f'{fuel_spent_2} fuel spent')


if __name__ == '__main__':
    solve()
