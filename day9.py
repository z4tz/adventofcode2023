import os
from inputreader import aocinput


def get_derivative(line: list[int]) -> list[int]:
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def extrapolated_oasis(data: list[str]) -> tuple[int, int]:
    total_future = 0
    total_past = 0
    for line in data:
        histories = [[int(value) for value in line.split()]]
        while not all(value == 0 for value in histories[-1]):
            histories.append(get_derivative(histories[-1]))
        future_value = 0
        past_value = 0
        for i in reversed(range(1, len(histories))):
            future_value += histories[i - 1][-1]
            past_value = histories[i - 1][0] - past_value
        total_future += future_value
        total_past += past_value

    return total_future, total_past


def main(day: int):
    data = aocinput(day)
    result = extrapolated_oasis(data)
    print(result)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
