import os
from inputreader import aocinput


def scratch_points(data: list[str]) -> tuple[int, int]:
    total_points = 0
    scratch_count = [1] * len(data)
    for i, line in enumerate(data):
        winners, numbers = line.split(':')[-1].split('|')
        winners = {int(winner) for winner in winners.split()}
        numbers = {int(number) for number in numbers.split()}
        match_count = sum(winner in numbers for winner in winners)

        total_points += 2 ** (match_count - 1) if match_count > 0 else 0  # part 1

        for j in range(i+1, i + match_count+1):
            scratch_count[j] += scratch_count[i]

    return total_points, sum(scratch_count)


def main(day: int):
    data = aocinput(day)
    result = scratch_points(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
