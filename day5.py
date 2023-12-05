import os
from inputreader import aocinput


def seed_location(data: list[str]) -> tuple[int, int]:
    seeds = [int(part) for part in data[0].split(':')[-1].split()]
    charts = []  # chart since map is python builtin
    for line in data[1:]:
        if line.strip().endswith(':'):
            chart = []
            charts.append(chart)
        elif len(line) > 1:
            chart.append([int(part) for part in line.split()])

    # part 1
    locations = get_locations(charts, seeds)
    # part 2
    seed_ranges = [(start, start + length - 1) for start, length in zip(seeds[::2], seeds[1::2])]
    location_ranges = get_location_ranges(charts, seed_ranges)

    return min(locations), min(start for start, end in location_ranges)


def get_locations(charts, seeds):
    locations = []
    for seed in seeds:
        source = seed
        for chart in charts:
            for line in chart:
                if line[1] <= source <= line[1] + line[2]:
                    source = source - line[1] + line[0]
                    break

        locations.append(source)
    return locations


def get_location_ranges(charts, seed_ranges):
    for chart in charts:
        converted_ranges = []  # seed ranges that matched with a chart
        for line in chart:
            remaining_ranges = []  # parts of seed ranges that weren't matched with a chart, try match with next line
            for seed_range in seed_ranges:
                if seed_range[0] >= line[1] + line[2] or seed_range[1] < line[1]:  # seed_range not affected
                    remaining_ranges.append(seed_range)

                elif seed_range[0] >= line[1] and seed_range[1] < line[1] + line[2]:  # seed_range all affected
                    converted_ranges.append((seed_range[0] - (line[1] - line[0]), seed_range[1] - (line[1] - line[0])))

                elif seed_range[0] < line[1] and seed_range[1] >= line[1] + line[2]:  # seed_range both above and below
                    remaining_ranges.append((seed_range[0], line[1]-1))  # below
                    converted_ranges.append((line[0], line[0] + line[2] - 1))  # inside
                    remaining_ranges.append((line[1]+line[2], seed_range[1]))  # above

                elif seed_range[0] >= line[1]:  # seed_range start inside end above
                    converted_ranges.append((line[0]+(seed_range[0]-line[1]), line[0]+line[2] - 1))  # inside
                    remaining_ranges.append((line[1]+line[2], seed_range[1]))  # above

                elif seed_range[1] < line[1] + line[2]:  # seed_range start below end inside
                    remaining_ranges.append((seed_range[0], line[1]-1))  # below
                    converted_ranges.append((line[0], line[0]+(seed_range[1]-line[1])))  # inside
                else:
                    print('shouldnt reach this', seed_range)

            seed_ranges = remaining_ranges
        seed_ranges = converted_ranges + remaining_ranges
    return seed_ranges


def main(day: int):
    data = aocinput(day)
    result = seed_location(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
