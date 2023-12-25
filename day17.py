import os
from inputreader import aocinput
import heapq

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def heat_loss(data: list[str], min_straight: int, max_straight: int) -> int:
    goal = (len(data[0].strip())-1, len(data)-1)
    data = {(x, y): int(char) for y, line in enumerate(data) for x, char in enumerate(line.strip())}
    seen = dict()
    queue = [(0, 0, 0, 0), (0, 0, 0, 1)]  # (heat, x, y, direction)
    heapq.heapify(queue)
    while queue:
        heat, x, y, direction = heapq.heappop(queue)
        if (x, y) == goal:
            return heat
        dx = directions[direction][0]
        dy = directions[direction][1]
        for i in range(1, max_straight+1):
            x += dx
            y += dy
            heat_temp = data.get((x, y))
            if heat_temp is None:
                break
            heat += heat_temp
            if i >= min_straight:
                for temp_direction in [(direction + 1) % 4, (direction - 1) % 4]:
                    if (location_direction := (x, y, temp_direction)) not in seen or seen[location_direction] > heat:
                        seen[location_direction] = heat
                        heapq.heappush(queue, (heat, x, y, temp_direction))


def main(day: int):
    data = aocinput(day)
    results = heat_loss(data, 1, 3)
    results2 = heat_loss(data, 4, 10)
    print(results, results2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
