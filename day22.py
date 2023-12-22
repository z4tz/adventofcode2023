import os
from inputreader import aocinput
from collections import defaultdict, deque


class Node:
    def __init__(self, node_id: int):
        self.id = node_id
        self.supported_by = set()
        self.supports = set()

    def __repr__(self):
        return f'Node {self.id}: supported by {self.supported_by} - supporting {self.supports}'


def disintegrate_bricks(data: list[str]) -> tuple[int, int]:
    nodes = dict()
    floating = []
    landed = dict()
    for i, line in enumerate(data):
        part1, part2 = line.split('~')
        part1 = part1.split(',')
        part2 = part2.split(',')
        brick = []

        for x in range(int(part1[0]), int(part2[0]) + 1):
            for y in range(int(part1[1]), int(part2[1]) + 1):
                for z in range(int(part1[2]), int(part2[2]) + 1):
                    brick.append([x, y, z])
        floating.append(brick)
    floating.sort(key=lambda a: a[0][2])

    highest = defaultdict(int)

    for i, brick in enumerate(floating):
        nodes[i] = Node(i)

        z_values = []
        for x, y, z in brick:
            z_values.append(highest[(x, y)])
        fall = brick[0][2] - max(z_values) - 1
        for x, y, z in brick:
            landing_z = z - fall
            highest[(x, y)] = landing_z

            if (cube_below := (x, y, landing_z - 1)) in landed and landed[cube_below] != i:
                nodes[i].supported_by.add(landed[cube_below])
                nodes[landed[cube_below]].supports.add(i)

            landed[(x, y, landing_z)] = i

    total = 0
    total2 = 0
    for i in nodes:
        falling = {i}
        current_falling = deque([i])
        while current_falling:
            current = nodes[current_falling.pop()]
            for above in current.supports:
                if all([supporting_node in falling for supporting_node in nodes[above].supported_by]):
                    current_falling.append(above)
                    falling.add(above)

        falling_count = len(falling) - 1
        if falling_count == 0:  # if no bricks would fall
            total += 1
        total2 += falling_count

    return total, total2


def main(day: int):
    data = aocinput(day)
    results = disintegrate_bricks(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
