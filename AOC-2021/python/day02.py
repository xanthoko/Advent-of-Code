from typing import List

from utils import get_input_text


def get_input_list() -> List[str]:
    input_text = get_input_text(2)
    splited_str_input_list = input_text.split('\n')
    return splited_str_input_list


def get_position_1(commands: List[str]) -> int:
    depth = 0
    horizontal = 0
    DEPTH_MAP = {'up': -1, 'down': 1}

    for command in commands:
        definition, value = command.split(' ')
        value = int(value)

        if definition == 'forward':
            horizontal += value
        else:
            depth += DEPTH_MAP[definition] * value

    return horizontal * depth


def get_position_2(commands: List[str]) -> int:
    aim = 0
    depth = 0
    horizontal = 0
    AIM_MAP = {'up': -1, 'down': 1}

    for command in commands:
        definition, value = command.split(' ')
        value = int(value)

        if definition == 'forward':
            horizontal += value
            depth += aim * value
        else:
            aim += AIM_MAP[definition] * value

    return horizontal * depth


def solve():
    commands = get_input_list()

    # PART 1
    position_1 = get_position_1(commands)
    print(f'Multiplied position is {position_1}')

    # PART 2
    position_2 = get_position_2(commands)
    print(f'Multiplied position is {position_2}')


if __name__ == '__main__':
    solve()
