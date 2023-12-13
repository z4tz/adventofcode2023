import os
from inputreader import aocinput
import numpy as np


def reflections(data: list[str]) -> tuple[int, int]:
    patterns = [[]]
    for line in data:
        if len(line) > 1:
            patterns[-1].append(line.strip())
        else:
            patterns.append([])
    result = 0
    result2 = 0
    for pattern_data in patterns:

        pattern = np.array([[value for value in line.strip()] for line in pattern_data])
        for i in range(1, pattern.shape[0]):  # horizontal comparison
            row_count = min([i, pattern.shape[0]-i])
            index_count = row_count * pattern.shape[1]
            equal_count = sum(sum(np.equal(pattern[i-row_count:i, :], np.flipud(pattern[i:i+row_count, :]))))
            if equal_count == index_count:
                result += i * 100
            if equal_count == index_count - 1:
                result2 += i * 100

        for i in range(1, pattern.shape[1]):  # vertical comparison
            column_count = min([i, pattern.shape[1]-i])
            index_count = column_count * pattern.shape[0]
            equal_count = sum(sum(np.equal(pattern[:, i-column_count:i], np.fliplr(pattern[:, i:i+column_count]))))
            if equal_count == index_count:
                result += i
            if equal_count == index_count - 1:
                result2 += i

    return result, result2


def main(day: int):
    data = aocinput(day)
    result = reflections(data)
    result2 = 0
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
