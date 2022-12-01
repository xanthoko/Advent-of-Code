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
    session_cookie = '53616c7465645f5f7c93f7f1391c4dc21b16da40630aec431a079c4103512ea'\
        '174f708e9795f1aaeec189f979c9d8f8d7f1e837a367cb6e9cdf057d4a3c9bbd7'
    cookies = {'session': session_cookie}

    url_day = day
    if day[0] == '0':
        url_day = day[1:]

    try:
        resp = requests.get(f'https://adventofcode.com/2022/day/{url_day}/input',
                            cookies=cookies)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Could not connect to url')
        raise ConnectionError

    if resp.status_code == 400:
        print(f'[ERROR] {resp.text}')
        raise ValueError('Invalid session cookie')

    with open(f'../inputs/day{day}.txt', 'w') as f:
        f.write(resp.text[:-1])  # remove the last \n


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Must specify day')
    else:
        download_input_from_url(sys.argv[1])
