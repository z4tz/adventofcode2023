import os


def aocinput(day: int) -> list[str]:
    with open(f'inputs/day{day}.txt') as f:
        lines = f.readlines()
    return lines


def day_has_inputs(day: int) -> bool:
    return os.path.isfile(f'inputs/day{day}.txt')
