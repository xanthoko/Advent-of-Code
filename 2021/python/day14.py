from typing import Dict, Tuple
from collections import defaultdict, Counter

from utils import get_input_text

EXAMPLE_INPUT = '''\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''
# EXPECTED_1 = 1588
# EXPECTED_2 =


def get_input_data(example=False) -> Tuple[str, Dict[str, str]]:
    if example:
        input_text = EXAMPLE_INPUT
    else:
        input_text = get_input_text(14)

    template, rules_s = input_text.strip().split('\n\n')
    rules_s = [x for x in rules_s.split('\n')]
    rules = {}
    for rule_s in rules_s:
        a, b = rule_s.split(' -> ')
        rules[a] = b
    return template, rules


template, rules = get_input_data()


def _make_step(bichar_counter: defaultdict,
               char_counter: Counter) -> defaultdict:
    tbc = bichar_counter.copy()  # length changes during iteration error !
    for key, value in bichar_counter.items():
        fc, sc = key
        insertion_char = rules[key]
        new_pair_1 = fc + insertion_char
        new_pair_2 = insertion_char + sc

        tbc[key] -= value
        tbc[new_pair_1] += value
        tbc[new_pair_2] += value

        char_counter[insertion_char] += value

        if tbc[key] == 0:
            tbc.pop(key)

    return tbc


def simulate_steps(steps: int) -> Counter:
    bichar_counter = defaultdict(int)
    for i in range(len(template) - 1):
        bichar_counter[template[i:i + 2]] += 1
    char_counter = Counter(template)

    for _ in range(steps):
        bichar_counter = _make_step(bichar_counter, char_counter)

    return char_counter


def solve_1() -> int:
    char_counter = simulate_steps(10)
    return char_counter.most_common()[0][1] - char_counter.most_common()[-1][1]


def solve_2() -> int:
    char_counter = simulate_steps(40)
    return char_counter.most_common()[0][1] - char_counter.most_common()[-1][1]


def solve():
    part_1 = solve_1()
    print(f'Part 1: {part_1}')

    part_2 = solve_2()
    print(f'Part 2: {part_2}')


if __name__ == '__main__':
    solve()
