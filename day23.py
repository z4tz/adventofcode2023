import os
from inputreader import aocinput


def hike_length(data: list[str]) -> tuple[int, int]:
    start = 1 + 0j
    end = complex(len(data[0].strip()) - 2, len(data) - 1)
    data = {complex(x, y): char for y, line in enumerate(data) for x, char in enumerate(line.strip()) if char != '#'}
    result1 = slippery_hike_length(data, start, end)
    result2 = non_slippery_hike_length(data, start,end)

    return result1, result2


def slippery_hike_length(data: dict[complex, str], start: complex, end: complex) -> int:
    to_visit = [(start, None)]
    steps = 0
    reached_end = []
    while to_visit:
        next_visit = []
        for current, previous in to_visit:
            if current == end:
                reached_end.append(steps)
                continue
            for direction, allowed in [(1, '>'), (1j, 'v'), (-1, '<'), (-1j, None)]:
                if (temp_position := current + direction) in data and temp_position != previous and (data[temp_position] == '.' or data[temp_position] == allowed):
                    next_visit.append((temp_position, current))
        steps += 1
        to_visit = next_visit
    return max(reached_end)


class Node:
    def __init__(self, name):
        self.name = name
        self.connections: dict[Node, int] = dict()

    def __repr__(self):
        return f'Name: {self.name} - Connections:{[length for length in self.connections.values()]}'


def non_slippery_hike_length(data: dict[complex, str], start: complex, end: complex) -> int:
    nodes = dict()
    nodes[start] = Node(start)
    seen = {start}
    new_paths = [(start, nodes[start])]
    while new_paths:
        current, from_node = new_paths.pop()
        origin = from_node.name
        steps = 1
        while True:
            if current == end:
                if current not in nodes:
                    nodes[current] = Node(current)
                nodes[current].connections[from_node] = steps
                from_node.connections[nodes[current]] = steps
                break
            neighbors = [neighbor for direction in [1, 1j, -1, -1j] if (neighbor := current + direction) in data]
            if len(neighbors) >= 3:
                if current not in nodes:
                    nodes[current] = Node(current)
                nodes[current].connections[from_node] = steps
                from_node.connections[nodes[current]] = steps
                for neighbor in neighbors:
                    if neighbor not in seen:
                        new_paths.append((neighbor, nodes[current]))
                break
            else:
                seen.add(current)
                neighbors = [neighbor for neighbor in neighbors if neighbor not in seen and neighbor != origin]
                if neighbors:
                    current = neighbors[0]
                    steps += 1
                else:
                    break

    def recursive_paths(current_node: Node, total_distance: int, visited: set[Node]):
        if current_node == end_node:
            distances.append(total_distance)
            return
        visited.add(current_node)
        for next_node, distance in current_node.connections.items():
            if next_node not in visited:
                recursive_paths(next_node, total_distance+distance, visited.copy())

    end_node = nodes[end]  # fetch end node once to save 2-3s runtime
    distances = []
    recursive_paths(nodes[start], 0, set())

    return max(distances) - 1


def main(day: int):
    data = aocinput(day)
    results = hike_length(data)
    print(results)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
