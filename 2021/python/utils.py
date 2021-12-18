import requests


def get_input_text(day):
    with open(f'../inputs/day{day:02}.txt', 'r') as f:
        return f.read()


def get_example_input_text():
    with open('../inputs/example.txt', 'r') as f:
        return f.read()


def get_input_text_from_url(day):
    """
    Returns:
        string: The text of the response (puzzle input)
    Raises:
        ValueError: Session cookie is invalid
    """
    session_cookie = '53616c7465645f5f1f96053cb690c9c84213d85d199789b6d7c3c4545a7'\
                     '189d07e962cc6fbb0dc9dfcae08df56ccc9c0'
    cookies = {'session': session_cookie}

    try:
        resp = requests.get(f'https://adventofcode.com/2021/day/{day}/input',
                            cookies=cookies)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Could not connect to url')
        raise ConnectionError

    if resp.status_code == 400:
        print(f'[ERROR] {resp.text}')
        raise ValueError('Invalid session cookie')

    return resp.text[:-1]  # remove the last \n
