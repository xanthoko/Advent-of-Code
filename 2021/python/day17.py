from typing import Tuple

from utils import get_input_text

EXAMPLE_INPUT = '''\
target area: x=20..30, y=-10..-5
'''
# EXPECTED_1 = 45
# EXPECTED_2 = 112


def get_input_data(example=False) -> Tuple[int, int, int, int]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(17)

    area_split = input_text.strip().split(' ')[2:]
    x_area = area_split[0][:-1].split('..')
    y_area = area_split[1].split('..')
    x1 = int(x_area[0][2:])
    x2 = int(x_area[1])
    y1 = int(y_area[0][2:])
    y2 = int(y_area[1])
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)
    return xmin, xmax, ymin, ymax


xmin, xmax, ymin, ymax = get_input_data()


def _get_x_step_size(velocity: int, step: int) -> int:
    # taking into consideration the drag (step - 1 or 0)
    if velocity > 0:
        return max(0, velocity - (step - 1))
    else:
        return min(0, velocity + (step - 1))


def _get_y_step_size(velocity: int, step: int) -> int:
    return velocity - (step - 1)


def _in_target_area(x: int, y: int) -> bool:
    return xmin <= x <= xmax and ymin <= y <= ymax


def _will_be_in_area(vel_x: int,
                     vel_y: int) -> Tuple[bool, Tuple[int, int], int]:
    x = 0
    y = 0
    step = 1
    max_y_pos = y
    while y > ymin and x < xmax:
        x += _get_x_step_size(vel_x, step)
        y += _get_y_step_size(vel_y, step)
        max_y_pos = max(max_y_pos, y)
        if _in_target_area(x, y):
            return True, (x, y), max_y_pos
        step += 1
    return False, (x, y), None


def _get_y_vel_for_x(vel_x: int) -> Tuple[int, int]:
    valid_velocities = []
    vel_y = ymin - 1  # init velocity lower than min y is not possible
    cand_vel_y = vel_y - 1

    while vel_y < 200:  # 200 is arbitrary, can't find something solid
        hit, critical_coords, max_y = _will_be_in_area(vel_x, vel_y)

        if hit:
            cand_vel_y = max(max_y, cand_vel_y)
            valid_velocities.append((vel_x, vel_y))
        elif critical_coords[0] > xmax:
            break
        vel_y += 1
    return cand_vel_y, valid_velocities


def solve_1() -> int:
    max_y_pos = []
    for vel_x in range(1, xmin):
        vel_y, _ = _get_y_vel_for_x(vel_x)
        max_y_pos.append(vel_y)
    return max(max_y_pos)


def solve_2() -> int:
    valid_velocities = []
    for vel_x in range(1, xmax + 1):
        _, all_y = _get_y_vel_for_x(vel_x)
        valid_velocities.extend(all_y)
    return len(valid_velocities)


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
