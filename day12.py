import os
from inputreader import aocinput


def cache_results(func):  # own implementation of functools cache, slower but learning is fun!
    cached_calls = dict()

    def wrapper(*args, **kwargs):
        if args in cached_calls:
            return cached_calls[args]
        result = func(*args, **kwargs)
        cached_calls[args] = result
        return result

    return wrapper


@cache_results
def recursive_springs(groups: tuple[int, ...], springs: str) -> int:
    if len(groups) == 0:
        return '#' not in springs  # if no # left it's a successful match

    if len(springs) == 0:
        return len(groups) == 0  # if empty, successful solution

    if springs.startswith('.'):
        return recursive_springs(groups, springs.lstrip('.'))

    if springs.startswith('?'):  # check both cases, dot can be space as it would only be removed directly again
        return (recursive_springs(groups, springs.replace('?', '', 1)) +
                recursive_springs(groups, springs.replace('?', '#', 1)))

    if springs.startswith('#'):
        if groups[0] > len(springs):
            return 0  # not enough space left to check for spring
        if '.' in springs[:groups[0]]:  # if not enough space to create current group
            return 0
        if springs[groups[0]] == '#':  # group too long
            return 0
        return recursive_springs(groups[1:], springs[groups[0] + 1:])  # group matched


def spring_arrangements(data: list[str], repeat: int = 1) -> int:
    arrangement_count = []
    for i, line in enumerate(data):
        springs, groups = line.split()
        springs = '?'.join([springs] * repeat)
        groups = tuple(int(value) for value in groups.split(',')) * repeat
        arrangement_count.append(recursive_springs(groups, springs + '.'))
    return sum(arrangement_count)


def main(day: int):
    data = aocinput(day)
    result = spring_arrangements(data)
    result2 = spring_arrangements(data, 5)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
