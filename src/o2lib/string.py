from pprint import pprint

__all__ = [
    'split_numbers',
]


def split_numbers(text, negative=False):
    groups = []
    number = ""
    last_non_digit = ""
    for c in f"{text} ":
        if c.isdigit():
            number = f"{number}{c}"
        else:
            if number:
                if negative and last_non_digit == "-":
                    number = f"-{number}"
                groups.append(number)
                number = ""
            last_non_digit = c
    return groups
