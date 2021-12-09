from utils import get_input_text

input_list = get_input_text(1)
masses = list(map(int, input_list.split('\n')))

fuels = [x // 3 - 2 for x in masses]
print(f'[PART 1] The sum is {sum(fuels)}')


def get_fuel(mass: int) -> int:
    fuel = mass // 3 - 2
    tf = 0
    while fuel > 0:
        tf += fuel
        fuel = fuel // 3 - 2
    return tf


total_fuel = [get_fuel(x) for x in masses]
print(f'[PART 2] The sum is {sum(total_fuel)}')
