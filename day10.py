import os
from inputreader import aocinput
import numpy as np

pipes = {'|': (1, 3),
         '-': (0, 2),
         'L': (0, 3),
         'J': (2, 3),
         '7': (1, 2),
         'F': (0, 1)}

directions = {0: (0, 1),
              1: (1, 0),
              2: (0, -1),
              3: (-1, 0)}


def add_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def pipe_distance(data: list[str]) -> tuple[int, int]:
    tiles = np.array([[value for value in line.strip()] for line in data])
    x_max = len(data[0].strip())
    y_max = len(data)
    start = tuple(np.argwhere(tiles == 'S')[0])
    visited = {start}
    to_visit = set()
    steps = 0

    for direction in (0, 1, 2, 3):  # find connecting neighbors to start square
        neighbor = add_tuples(start, directions[direction])
        if (direction + 2) % 4 in pipes[tiles[neighbor]]:  # neighbor has pipe in direction of start
            to_visit.add(neighbor)
    while to_visit:
        next_visits = set()
        for coordinate in to_visit:
            for direction in pipes[tiles[coordinate]]:
                connected_coordinate = add_tuples(coordinate, directions[direction])
                if connected_coordinate not in visited:
                    next_visits.add(connected_coordinate)
            visited.add(coordinate)
        to_visit = next_visits
        steps += 1

    # part 2, count number of vertical pipes to the left of a square, if odd it's enclosed by the loop
    enclosed = 0
    for y in range(1, y_max):  # edge can be skipped, never enclosed
        pipe_count = 0
        previous_bend = ''
        for x in range(x_max + 1):
            current = (y, x)
            if current in visited:
                current_tile = tiles[current]
                if current_tile == '|':
                    pipe_count += 1
                elif current_tile in ['F', 'L']:
                    previous_bend = current_tile
                elif (current_tile == 'J' and previous_bend == 'F') or (current_tile == '7' and previous_bend == 'L'):
                    pipe_count += 1
            elif pipe_count % 2:  # if odd pipe count
                enclosed += 1
    return steps, enclosed


def main(day: int):
    data = aocinput(day)
    result = pipe_distance(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
