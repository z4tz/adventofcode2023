import os
from inputreader import aocinput


def part_numbers(data: list[str]) -> tuple[int, int]:
    schematic_width = len(data[0])

    def get_part_location(x_coord: int, y_coord: int) -> tuple[int, int, int]:
        x_low = x_coord
        x_high = x_coord
        while data[y_coord][x_low - 1].isnumeric() and x_low > 0:
            x_low -= 1
        while data[y_coord][x_high + 1].isnumeric() and x_low < schematic_width:
            x_high += 1
        return y_coord, x_low, x_high + 1

    part_locations = set()
    gears = []
    for y, line in enumerate(data):
        for x, char in enumerate(line.strip()):
            gear_identifier = set()
            if not data[y][x].isnumeric() and data[y][x] != '.':
                for x_diff, y_diff in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
                    try:
                        if data[y + y_diff][x + x_diff].isnumeric():
                            location = get_part_location(x + x_diff, y + y_diff)
                            part_locations.add(location)
                            if data[y][x] == '*':
                                gear_identifier.add(location)
                    except IndexError:
                        continue
            if len(gear_identifier) == 2:
                gear_numbers = [int(data[y][x_min:x_max]) for y, x_min, x_max in gear_identifier]
                gears.append(gear_numbers[0]*gear_numbers[1])

    total = sum(int(data[y][x_min:x_max]) for y, x_min, x_max in part_locations)
    return total, sum(gears)


def main(day: int):
    data = aocinput(day)
    result = part_numbers(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
