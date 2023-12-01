import os
import re

from inputreader import aocinput


def calibration_values(data: list[str]) -> int:
    total = 0
    for line in data:
        digits = re.findall(r'(\d)', line)
        total += int(digits[0] + digits[-1])
    return total


def calibration_values_alphanum(data: list[str]) -> int:
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    replacements = [number + str(i + 1) + number for i, number in enumerate(numbers)]
    total = 0
    for line in data:
        for i, number in enumerate(numbers):
            line = line.replace(number, replacements[i])
        digits = re.findall(r'(\d)', line)
        total += int(digits[0] + digits[-1])
    return total


def main(day: int):
    data = aocinput(day)
    result = calibration_values(data)
    result2 = calibration_values_alphanum(data)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
