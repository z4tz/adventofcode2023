import os
from inputreader import aocinput
from collections import deque, defaultdict


def energized_tiles(data: list[str], size=None, start: tuple[complex, complex] = (0 + 0j, 1)) -> int:
    if size is None:
        size = (len(data[0]), len(data))
    to_move: deque[tuple[complex, complex]] = deque([start])
    visited = set()
    while to_move:
        location, direction = to_move.pop()
        if 0 > location.real or size[0] <= location.real or 0 > location.imag or size[1] <= location.imag or (
                location, direction) in visited:
            continue  # skip value outside field or already visited
        tile = data[int(location.imag)][int(location.real)]
        visited.add((location, direction))
        if tile == '.':
            to_move.append((location + direction, direction))
        elif tile == '/':
            if direction.real:
                direction *= -1j
            else:
                direction *= 1j
            to_move.append((location + direction, direction))
        elif tile == '\\':
            if direction.real:
                direction *= 1j
            else:
                direction *= -1j
            to_move.append((location + direction, direction))
        elif tile == '|':
            if direction.real:
                to_move.append((location + 1j, 1j))
                to_move.append((location + -1j, -1j))
            else:
                to_move.append((location + direction, direction))
        elif tile == '-':
            if direction.imag:
                to_move.append((location + 1, 1))
                to_move.append((location + -1, -1))
            else:
                to_move.append((location + direction, direction))

    energized = len(set([location for location, direction in visited]))
    return energized


def best_configuration(data: list[str]) -> int:
    results = []
    size = (len(data[0]), len(data))
    for x in range(size[0]):
        results.append(energized_tiles(data, size, start=(x+0j, 1j)))
        results.append(energized_tiles(data, size, start=(complex(x, size[1]-1), -1j)))
    for y in range(size[1]):
        results.append(energized_tiles(data, size, start=(complex(0, y), 1)))
        results.append(energized_tiles(data, size, start=(complex(size[0]-1, y), -1)))
    return max(results)


def main(day: int):
    data = aocinput(day)
    data = [line.strip() for line in data]
    result = energized_tiles(data)
    results2 = best_configuration(data)
    print(result, results2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
