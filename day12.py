import os
from inputreader import aocinput
from collections import Counter
from itertools import permutations


def spring_arrangements(data: list[str]) -> int:
    for line in data:
        springs, groups = line.split()
        groups = [int(value) for value in groups.split(',')]
        counter = Counter(springs)
        damaged_to_add = sum(groups) - counter['#']
        operational_to_add = counter['?'] - damaged_to_add
        to_add = ['#'] * damaged_to_add + ['.'] * operational_to_add
        print(set(permutations(to_add, len(to_add))))





def main(day: int):
    data = aocinput(day)
    result = spring_arrangements(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
