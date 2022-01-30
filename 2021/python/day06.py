from typing import List

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(6)
    splited_str_input_list = list(map(int, input_text.strip().split(',')))
    return splited_str_input_list


def get_number_of_fish_after_n_days(intervals: List[str], days: int) -> int:
    total_population = 0
    for interval in intervals:
        population_from_current_fish = 1 + _babies_born_in_days(interval, days)
        total_population += population_from_current_fish
    return total_population


def _babies_born_in_days(initial_state: int, number_of_days: int, cache={}) -> int:
    if number_of_days < initial_state:
        # no time to give birth
        return 0
    else:
        full_cycle_start = number_of_days - initial_state - 1
        # full cycle babies (7 days) + 1 from the initial state
        newborn_babies = full_cycle_start // 7 + 1

        # for every newborn calculate its own babies
        for i in range(newborn_babies):
            baby_days = full_cycle_start - i * 7
            if (8, baby_days) in cache:
                grandbabies = cache[(8, baby_days)]
            else:
                grandbabies = _babies_born_in_days(8, baby_days, cache)
                cache[(8, baby_days)] = grandbabies
            newborn_babies += grandbabies

        return newborn_babies


def solve():
    intervals = get_input_list()

    # PART 1
    fish_1 = get_number_of_fish_after_n_days(intervals, 80)
    print(f'{fish_1} laternfish after 80 days')

    # PART 2
    fish_2 = get_number_of_fish_after_n_days(intervals, 256)
    print(f'{fish_2} laternfish after 256 days')


if __name__ == '__main__':
    solve()
