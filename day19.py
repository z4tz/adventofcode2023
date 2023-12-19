import os
from inputreader import aocinput
import operator
from functools import reduce

categories = {'x': 0,
              'm': 1,
              'a': 2,
              's': 3}
operations = {'>': operator.gt,
              '<': operator.lt}


def rating_numbers(data: list[str]) -> int:
    workflows = dict()
    machine_parts = []

    for line in data:
        if line.startswith('{'):
            machine_parts.append(tuple(int(p[2:]) for p in line.strip()[1:-1].split(',')))
        elif len(line) > 1:
            name, rest = line.split('{')
            parts = rest[:-1].split(',')
            rules = []
            for part in parts[:-1]:
                part, send_to = part.split(':')
                rules.append((categories[part[0]], operations[part[1]], int(part[2:]), send_to))
            rules.append(parts[-1][:-1])
            workflows[name] = rules

    accepted_parts = 0
    for part in machine_parts:
        current = 'in'
        while current not in ['A', 'R']:
            rules = workflows[current]
            current = work(part, rules)

        if current == 'A':
            accepted_parts += sum(part)
    return accepted_parts


def work(part: tuple[int, ...], rules: list[tuple[[int, callable, int, str]]]) -> str:
    for rule in rules:
        if type(rule) is str:
            return rule
        if rule[1](part[rule[0]], rule[2]):
            return rule[3]


def accepted_combinations(data: list[str]) -> int:
    workflows = dict()
    for line in data:
        if line.strip() == '':
            break
        name, rest = line.split('{')
        parts = rest[:-1].split(',')
        rules = []
        for part in parts[:-1]:
            part, send_to = part.split(':')
            rules.append((part[0], part[1], int(part[2:]), send_to))
        rules.append(parts[-1][:-1])
        workflows[name] = rules
    part_combinations = []

    def accepted_parts_recursive(name: str, limits: list) -> None:
        if name in ['A', 'R']:
            if name == 'A':
                part_combinations.append(limits)
            return

        for rule in workflows[name]:
            if type(rule) is tuple:
                limits_copy = [limit[:] for limit in limits]  # "deep" copy of limits
                if rule[1] == '>':
                    limits_copy[categories[rule[0]]][0] = rule[2] + 1
                    limits[categories[rule[0]]][1] = rule[2]
                else:
                    limits_copy[categories[rule[0]]][1] = rule[2] - 1
                    limits[categories[rule[0]]][0] = rule[2]
                accepted_parts_recursive(rule[3], limits_copy)
            else:
                accepted_parts_recursive(rule, limits)
    part_limits = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
    accepted_parts_recursive('in', part_limits)
    total = 0

    for combination in part_combinations:
        total += reduce(lambda a, b: a*b, [hi-low+1 for low, hi in combination])
    return total


def main(day: int):
    data = aocinput(day)
    results = rating_numbers(data)
    results2 = accepted_combinations(data)
    print(results, results2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
