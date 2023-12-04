import os
import re

from inputreader import aocinput


def possible_games(data: list[str], red: int, blue: int, green: int) -> int:
    game_sum = 0
    for line in data:
        game, cubes = line.split(':')
        for part in re.split(';|,', cubes):
            if 'red' in part and int(part.split()[0]) > red:
                break
            if 'blue' in part and int(part.split()[0]) > blue:
                break
            if 'green' in part and int(part.split()[0]) > green:
                break
        else:  # if for loop completes without any break
            game_sum += int(game.split()[1])
    return game_sum


def game_power(data: list[str]) -> int:
    total_power = 0
    for line in data:
        cube_minimum = [0, 0, 0]
        for part in re.split('[;,]', line.split(':')[1]):
            if 'red' in part:
                cube_minimum[0] = max([int(part.split()[0]), cube_minimum[0]])
            elif 'blue' in part:
                cube_minimum[1] = max([int(part.split()[0]), cube_minimum[1]])
            else:
                cube_minimum[2] = max([int(part.split()[0]), cube_minimum[2]])
        total_power += cube_minimum[0] * cube_minimum[1] * cube_minimum[2]
    return total_power


def main(day: int):
    data = aocinput(day)
    result = possible_games(data, 12, 14, 13)
    result2 = game_power(data)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
