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
    session_cookie = '53616c7465645f5fea48bce577ada3276f18328538cfa6954c4b5181e9af'\
        '6af99d04f5accf9716508ea63d44cba355ac8a6c8d04d1a1b7dbe693bed96f779044'
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
