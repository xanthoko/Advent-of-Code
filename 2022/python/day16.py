from __future__ import annotations

import argparse

from utils import get_input_text

EXAMPLE_INPUT = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED_1 = 1651
EXPECTED_2 = None

parser = argparse.ArgumentParser(prog='AoC')
parser.add_argument('-p',
                    '--production',
                    required=False,
                    const=True,
                    nargs='?',
                    default=False)
is_production = parser.parse_args().production


def get_input_data() -> None:
    if is_production:
        input_text = get_input_text(16)
    else:
        input_text = EXAMPLE_INPUT
    input_text.strip('\n')
    flow_rates = {}
    conn = {}
    for l in input_text.splitlines():
        splt = l.split(' ')
        valve = splt[1]
        flow_rates[valve] = int(splt[4][5:-1])
        conn[valve] = [x.strip(',') for x in splt[9:]]
    return flow_rates, conn


input_data = get_input_data()


def solve_1() -> int:
    flow_rates: list[int]
    conn: list[list[str]]
    flow_rates, conn = input_data
    # open_valves: set(str) = set()
    # time_remaining: int = 30

    best = {}
    todo = [('AA', set(), 30, 0, None)]
    while todo:
        valve, opened_valves, time_remaining, pressure, last = todo.pop(0)
        print(len(todo), time_remaining)
        best.setdefault(time_remaining, pressure)

        if time_remaining == 0:
            break

        if valve not in opened_valves:
            # open the valve
            ov = opened_valves.copy()
            ov.add(valve)
            pressure_released = flow_rates[valve] * (time_remaining - 1)
            new_pressure = pressure + pressure_released
            if new_pressure > best[time_remaining]:
                best[time_remaining] = new_pressure
            todo.append((valve, ov, time_remaining - 1,
                         pressure + pressure_released, valve))

        for neighbor in conn[valve]:
            if neighbor is last and last in opened_valves:
                todo.append(
                    (neighbor, opened_valves, time_remaining - 1, pressure, valve))
    print(best)


def solve_2() -> int:
    # TODO: implement solution here
    pass


def _validate(expected, actual):
    if not is_production:
        error_msg = f'\033[41mExpected: {expected}. Got: {actual}\033[m'
        assert actual == expected, error_msg


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')
    _validate(EXPECTED_1, part_1)

    part_2 = solve_2()
    print(f'Part 2: {part_2}')
    _validate(EXPECTED_2, part_2)


if __name__ == '__main__':
    solve()
