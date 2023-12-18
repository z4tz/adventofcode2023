import os
from inputreader import aocinput

directions = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}
hex_directions = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}


def area_by_shoelace(x, y):
    return abs(sum(x[i-1]*y[i]-x[i]*y[i-1] for i in range(len(x)))) / 2.


def instructions_to_area(instructions: list[tuple[str, int]]) -> int:
    x = 0
    y = 0
    x_list = []
    y_list = []

    total_distance = 0
    for direction, distance in instructions:
        dx, dy = directions[direction]
        x += dx * distance
        y += dy * distance
        x_list.append(x)
        y_list.append(y)
        total_distance += distance
    return int(area_by_shoelace(x_list, y_list) + total_distance/2 + 1)


def trench_area(data: list[str]) -> tuple[int, int]:
    instructions = []
    hex_instructions = []
    for line in data:
        direction, distance, hex_distance_string = line.strip().split()
        instructions.append((direction, int(distance)))
        hex_instructions.append((hex_directions[hex_distance_string[-2]], int(hex_distance_string[2:-2], 16)))
    return instructions_to_area(instructions), instructions_to_area(hex_instructions)


def main(day: int):
    data = aocinput(day)
    results = trench_area(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
