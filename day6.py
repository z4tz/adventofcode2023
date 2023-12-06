import os
from inputreader import aocinput
from functools import reduce
import math


def boat_races(data: list[str]) -> int:
    durations = [int(value) for value in data[0].split()[1:]]
    distances = [int(value) for value in data[1].split()[1:]]

    record_beaters = [0] * len(durations)

    for i in range(len(durations)):
        for button_time in range(durations[i] + 1):
            if button_time * (durations[i] - button_time) > distances[i]:
                record_beaters[i] += 1
    return reduce(lambda a, b: a * b, record_beaters)


def boat_race(data: list[str]) -> int:
    duration = int(data[0].split(':')[-1].replace(' ', ''))
    distance = int(data[1].split(':')[-1].replace(' ', ''))
    # solve  0 = t^2 - duration * t + distance where t is button time
    button_1 = math.ceil((duration + math.sqrt(math.pow(duration, 2) - 4 * distance)) / 2)
    button_2 = math.ceil((duration - math.sqrt(math.pow(duration, 2) - 4 * distance)) / 2)
    return abs(button_1-button_2)


def main(day: int):
    data = aocinput(day)
    result = boat_races(data)
    result2 = boat_race(data)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
