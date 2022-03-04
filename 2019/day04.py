range_min = 197487
range_max = 673251


def _is_valid_password(password: int) -> bool:
    str_pass = str(password)
    d = False
    for i in range(5):
        if str_pass[i] > str_pass[i + 1]:
            return False
        elif str_pass[i] == str_pass[i + 1]:
            d = True

    return d


pps = 0
for pp in range(range_min, range_max):
    pps += int(_is_valid_password(pp))

print(pps)
