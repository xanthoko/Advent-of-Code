from typing import List, Dict, Tuple
from collections import defaultdict

from utils import get_input_text

EXAMPLE_INPUT = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''
# EXPECTED_1 = 10
# EXPECTED_2 = 103


def get_input_data(example=False) -> defaultdict:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(12)

    lines = input_text.strip().splitlines()
    connections = defaultdict(list)
    for line in lines:
        p1, p2 = line.split('-')
        connections[p1].append(p2)
        connections[p2].append(p1)
    return connections


connections = get_input_data(True)


def solve_1(cave: str, visited=set()) -> int:
    if cave == 'end':
        return 1
    
    if cave.islower() and cave != 'end':
        visited.add(cave)
    connected_caves = [x for x in connections[cave] if x not in visited]

    total_paths_from_cave = 0
    for connected_cave in connected_caves:
        vv = visited.copy()
        total_paths_from_cave += solve_1(connected_cave, vv)
    return total_paths_from_cave


def solve_2() -> int:
    # TODO: implement solution here
    pass


def solve():
    # part 1
    part_1 = solve_1('start', set(['start']))
    print(f'Part 1: {part_1}')

    # part 2
    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
