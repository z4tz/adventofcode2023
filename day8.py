import os
from inputreader import aocinput
from itertools import cycle
from math import lcm


def steps(data: list[str]) -> tuple[int, int]:
    choices = cycle([0 if value == 'L' else 1 for value in data[0].strip()])
    elements = dict()
    for line in data[2:]:
        parts = line.split(' = ')
        elements[parts[0]] = parts[1][1:4], parts[1][6:9]

    # part 1
    current = 'AAA'
    counter = 0
    while current != 'ZZZ':
        current = elements[current][next(choices)]
        counter += 1

    # part 2
    start_elements = [element for element in elements if element[2] == 'A']
    step_counts = []
    for element in start_elements:
        choices = cycle([0 if value == 'L' else 1 for value in data[0].strip()])
        step_count = 0
        while element[2] != 'Z':
            element = elements[element][next(choices)]
            step_count += 1
        step_counts.append(step_count)
    return counter, lcm(*step_counts)


def main(day: int):
    data = aocinput(day)
    result = steps(data)
    result2 = 0
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
