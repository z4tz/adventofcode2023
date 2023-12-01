def aocinput(day: int) -> list[str]:
    with open(f'inputs/day{day}.txt') as f:
        lines = f.readlines()
    return lines
