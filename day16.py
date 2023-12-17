import os
from inputreader import aocinput
from collections import deque


def energized_tiles(data: dict[complex, str], start: tuple[complex, complex] = (0 + 0j, 1)) -> int:
    branches: deque[tuple[complex, complex]] = deque([start])
    visited = set()
    while branches:
        location, direction = branches.pop()
        while (location, direction) not in visited:
            tile = data.get(location)
            if tile is None:
                break
            visited.add((location, direction))
            if tile == '.':
                pass 
            elif tile == '/':
                direction = -complex(direction.imag, direction.real)
            elif tile == '\\':
                direction = complex(direction.imag, direction.real)
            elif tile == '|':
                if direction.real:
                    direction = -1j
                    branches.append((location + 1j, 1j))
            elif tile == '-':
                if direction.imag:
                    direction = 1
                    branches.append((location - 1, -1))
            location += direction

    energized = len(set([location for location, direction in visited]))
    return energized


def best_configuration(data: list[str]) -> tuple[int, int]:
    results = []
    size = (len(data[0].strip()), len(data))
    data = {complex(x, y): char for y, line in enumerate(data) for x, char in enumerate(line.strip())}
    for x in range(size[0]):
        results.append(energized_tiles(data, start=(x+0j, 1j)))
        results.append(energized_tiles(data, start=(complex(x, size[1]-1), -1j)))
    for y in range(size[1]):
        results.append(energized_tiles(data, start=(complex(0, y), 1)))
        results.append(energized_tiles(data, start=(complex(size[0]-1, y), -1)))
    return energized_tiles(data), max(results)


def main(day: int):
    data = aocinput(day)
    results = best_configuration(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
