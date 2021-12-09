from itertools import product

from utils import get_input_text

input_text = get_input_text(2)
int_input = list(map(int, input_text.split(',')))


def run_program(noun: int, verb: int) -> int:
    inst = int_input.copy()
    inst[1] = noun
    inst[2] = verb

    index = 0
    opcode = inst[index]
    while opcode != 99:
        num1 = inst[inst[index + 1]]
        num2 = inst[inst[index + 2]]
        inst[inst[index + 3]] = num1 + num2 if opcode == 1 else num1 * num2
        index += 4
        opcode = inst[index]
    return inst[0]


print(f'[PART 1] {run_program(12,2)} is at position 0')

for noun, verb in product(range(100), range(100)):
    if run_program(noun, verb) == 19690720:
        break
ans = 100 * noun + verb
print(f'[PART 2] {ans}')
