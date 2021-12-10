import pytest
from typing import List
from statistics import median

from utils import get_input_text, get_example_input_text

EXPECTED_1 = 26397
EXPECTED_2 = 288957

ERROR_SCORE_MAP = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORE_MAP = {')': 1, ']': 2, '}': 3, '>': 4}
FORWARD = {'(': ')', '[': ']', '{': '}', '<': '>'}
REVERSE = {v: k for k, v in FORWARD.items()}


def get_input_data(example=False):
    if example:
        input_text = get_example_input_text()
    else:
        input_text = get_input_text(10)
    return input_text.splitlines()


lines = get_input_data(True)


def get_syntax_error_score(lines: List[str]) -> int:
    syntax_score = 0
    for line in lines:
        open_chunks = []
        for c in line:
            if c in FORWARD:
                open_chunks.append(c)
            elif REVERSE[c] != open_chunks.pop():
                syntax_score += ERROR_SCORE_MAP[c]
                break

    return syntax_score


def get_completion_middle_score(lines: List[str]) -> int:
    scores = []
    for line in lines:
        line_score = 0
        open_chunks = []
        for c in line:
            if c in FORWARD:
                open_chunks.append(c)
            elif REVERSE[c] != open_chunks.pop():
                break
        else:
            for open_chunk in reversed(open_chunks):
                line_score *= 5
                line_score += COMPLETION_SCORE_MAP[FORWARD[open_chunk]]
            scores.append(line_score)

    return int(median(scores))


@pytest.mark.parametrize(
    ('input', 'expected'),
    ((get_input_data(example=True), EXPECTED_1), ),
)
def test_part_1(input: str, expected: int) -> None:
    assert get_syntax_error_score(input) == expected


@pytest.mark.parametrize(
    ('input', 'expected'),
    ((get_input_data(example=True), EXPECTED_2), ),
)
def test_part_2(input: str, expected: int) -> None:
    assert get_completion_middle_score(input) == expected


def main():
    # part 1
    syntax_error_score = get_syntax_error_score(lines)
    print(f'Part 1: {syntax_error_score}')

    # part 2
    completion_score = get_completion_middle_score(lines)
    print(f'Part 2: {completion_score}')


if __name__ == '__main__':
    main()
