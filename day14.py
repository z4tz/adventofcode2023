import os
from inputreader import aocinput
import numpy as np

rock_dict: dict[str, int] = {'O': 1,
                             '.': 2,
                             '#': 3}


def boulder_load(data: list[str]) -> tuple[int, int]:
    rocks = np.array([[rock_dict[value] for value in line.strip()] for line in data])
    stops = []  # calculate where square "stop points" are for round rocks, aka end points and square rocks
    for i in range(4):  # for each direction
        stops.append([])
        for column in rocks.transpose():
            stops[-1].append([-1] + np.where(column == 3)[0].tolist() + [len(column)])
        rocks = np.rot90(rocks, k=-1)

    tilt_platform(rocks, stops[0])
    rock_load = calculate_load(rocks)

    # part 2
    results = list()
    for i in range(300):
        for j in range(4):
            tilt_platform(rocks, stops[j])
            rocks = np.rot90(rocks, k=-1)
        if i >= 200:  # after arbitrary amount of cycles we should have a steady cycle
            result = calculate_load(rocks)
            if result in results:
                cycle = i - 200
                steps = (1_000_000_000 - 200) % cycle
                cycled_load = results[steps - 1]
                break
            else:
                results.append(result)

    return rock_load, cycled_load


def tilt_platform(rocks: np.array, stops: list[list[int]]) -> np.array:
    for i, column in enumerate(rocks.transpose()):
        for j in range(len(stops[i]) - 1):
            column[stops[i][j] + 1:stops[i][j + 1]].sort()  # sort parts between each square rock


def calculate_load(rocks: np.array) -> int:
    rock_load = 0
    for i, row in enumerate(rocks):
        rock_load += np.count_nonzero(row == 1) * (rocks.shape[0] - i)
    return rock_load


def main(day: int):
    data = aocinput(day)
    result = boulder_load(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
