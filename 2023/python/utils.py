import sys

import requests


def get_input_text(day):
    with open(f'../inputs/day{day:02}.txt', 'r') as f:
        return f.read()


def get_example_input_text():
    with open('../inputs/example.txt', 'r') as f:
        return f.read()


def download_input_from_url(day):
    """
    Returns:
        string: The text of the response (puzzle input)
    Raises:
        ValueError: Session cookie is invalid
    """
    session_cookie = '53616c7465645f5f7867a2df5d2ffd535d3a9f50be6ec0e9dff3d0dd92c'\
                    'e7e448e8500cdb3595b955e556ece286fa34e8b2d399e8a8f03f03e7d376e4b131d5d'
    cookies = {'session': session_cookie}

    try:
        resp = requests.get(f'https://adventofcode.com/2022/day/{day}/input',
                            cookies=cookies)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Could not connect to url')
        raise ConnectionError

    if resp.status_code == 400:
        print(f'[ERROR] {resp.text}')
        raise ValueError('Invalid session cookie')

    with open(f'../inputs/day{day:0>2}.txt', 'w') as f:
        f.write(resp.text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must specify day')
    else:
        download_input_from_url(sys.argv[1])
