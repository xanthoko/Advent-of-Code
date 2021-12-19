from os import path
from typing import List, Dict
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
# EXPECTED_2 = 36


def get_input_data(example=False) -> defaultdict:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(12)

    lines = input_text.strip().splitlines()
    connections = defaultdict(set)
    for line in lines:
        p1, p2 = line.split('-')
        connections[p1].add(p2)
        connections[p2].add(p1)
    return connections


connections = get_input_data()


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
    total_paths = set()
    todo = [(('start', ), False)]
    while todo:
        path, double_cave = todo.pop()

        if path[-1] == 'end':
            total_paths.add(path)
            continue

        for cand in connections[path[-1]]:
            if cand == 'start':
                continue
            elif cand.isupper() or cand not in path:
                todo.append(((*path, cand), double_cave))
            elif not double_cave and path.count(cand) == 1:
                todo.append(((*path, cand), True))
    return len(total_paths)


def solve():
    part_1 = solve_1('start')
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
