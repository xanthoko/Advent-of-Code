from typing import List
from statistics import median

from utils import get_input_text

ERROR_SCORE_MAP = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORE_MAP = {')': 1, ']': 2, '}': 3, '>': 4}
OPENERS = ['(', '[', '{', '<']
MATCHES = {')': '(', ']': '[', '}': '{', '>': '<'}
REVERSE_MATCHES = {v: k for k, v in MATCHES.items()}


def get_input_data() -> List[List[int]]:
    input_text = get_input_text(10)
    return input_text.splitlines()


lines = get_input_data()

# part 1
corrupted_lines = []
syntax_score = 0
for ind, line in enumerate(lines):
    open_chunks = []
    for c in line:
        if c in OPENERS:
            open_chunks.append(c)
        elif MATCHES[c] != open_chunks.pop():
            syntax_score += ERROR_SCORE_MAP[c]
            corrupted_lines.append(ind)
            break

print(f'Part 1: {syntax_score}')

# part 2
scores = []
for ind, line in enumerate(lines):
    if ind in corrupted_lines:
        continue

    line_score = 0
    open_chunks = []
    for c in line:
        if c in OPENERS:
            open_chunks.append(c)
        else:
            open_chunks.pop()

    for open_chunk in reversed(open_chunks):
        completion_char = REVERSE_MATCHES[open_chunk]
        line_score *= 5
        line_score += COMPLETION_SCORE_MAP[completion_char]

    scores.append(line_score)

print(f'Part 2: {median(scores)}')
