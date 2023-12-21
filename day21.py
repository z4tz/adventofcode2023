import os
from inputreader import aocinput


def garden_steps(data: list[str], part1: int, part2: int) -> tuple[int, int]:
    size = len(data[0].strip())  # same width and height
    garden = set()
    for y, line in enumerate(data):
        for x, char in enumerate(line.strip()):
            if char == '.':
                garden.add((x, y))
            if char == 'S':
                garden.add((x, y))
                start = (x, y)

    target = part2
    cycles = target // (size*2)  # cycle length 2x grid width/height for stable cycle increase
    remainder = target % (size*2)
    location_counts = []
    locations = [{start}, set()]
    prev_locations = {start}
    i = 0
    while len(location_counts) < 3 or i <= 300:  # at least 3 data points for part 2, example input needs more
        new_locations = set()
        for x, y in prev_locations:
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if ((x + dx) % size, (y + dy) % size) in garden:
                    if (neighbor := (x + dx, y + dy)) not in locations[(i+1) % 2]:
                        new_locations.add(neighbor)
        locations[(i+1) % 2].update(new_locations)
        prev_locations = new_locations
        if i == part1-1:
            result1 = len(locations[(i+1) % 2])
        if i % (size*2) == remainder:
            location_counts.append(len(locations[target % 2]))  # save count each cycle
        i += 1

    # find the delta count and delta delta count
    delta_count = [location_counts[i+1] - location_counts[i] for i in range(len(location_counts)-1)]
    delta_delta_count = [delta_count[i+1] - delta_count[i] for i in range(len(delta_count)-1)]

    total = location_counts[-1]
    increase = delta_count[-1]
    for i in range(cycles-len(location_counts)+1):
        increase += delta_delta_count[-1]
        total += increase

    return result1,  total


def main(day: int):
    data = aocinput(day)
    results = garden_steps(data, 64, 26501365)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
