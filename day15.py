import os
from inputreader import aocinput
import re
from functools import cache


def initialization_hash(data: list[str]) -> int:
    total = 0
    for part in data[0].strip().split(','):
        total += hash_value(part)
    return total


@cache
def hash_value(string):
    value = 0
    for char in string:
        value = (value + ord(char)) * 17 % 256
    return value


def lens_configuration(data: list[str]) -> int:
    boxes = [dict() for _ in range(256)]
    for part in data[0].strip().split(','):
        label, lens = re.split('=|-', part)
        box = hash_value(label)
        if '-' in part:
            if label in boxes[box]:
                del boxes[box][label]
        else:
            boxes[box][label] = lens
    power = 0
    for i, box in enumerate(boxes, 1):
        for j, focal_length in enumerate(box.values(), 1):
            power += i * j * int(focal_length)
    return power


def main(day: int):
    data = aocinput(day)
    result = initialization_hash(data)
    results2 = lens_configuration(data)
    print(result, results2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
