import os
from inputreader import aocinput
import numpy as np


def star_distance(data: list[str], space_expansion: int = 2) -> int:
    galaxy_map = np.array([[True if value == '#' else False for value in line.strip()] for line in data])
    galaxy_row_summation = galaxy_map.sum(axis=0)
    galaxy_column_summation = galaxy_map.sum(axis=1)
    empty_rows = np.where(galaxy_column_summation == 0)[0]
    empty_columns = np.where(galaxy_row_summation == 0)[0]
    galaxy_row_summation = [int(value) for value in galaxy_row_summation]  # cast to 64 bit int to prevent overflow
    galaxy_column_summation = [int(value) for value in galaxy_column_summation]

    x_distances = [space_expansion if x in empty_columns else 1 for x in range(galaxy_map.shape[0])]
    y_distances = [space_expansion if y in empty_rows else 1 for y in range(galaxy_map.shape[1])]

    total_distance: int = 0
    for i in range(galaxy_map.shape[0]):
        for j in range(i+1, galaxy_map.shape[0]):
            total_distance += galaxy_row_summation[i] * galaxy_row_summation[j] * (sum(x_distances[i:j]))
    for i in range(galaxy_map.shape[1]):
        for j in range(i+1, galaxy_map.shape[1]):
            total_distance += galaxy_column_summation[i] * galaxy_column_summation[j] * (sum(y_distances[i:j]))

    return total_distance


def main(day: int):
    data = aocinput(day)
    result = star_distance(data)
    result2 = star_distance(data, 1000000)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
