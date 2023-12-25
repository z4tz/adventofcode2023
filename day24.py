import os
from inputreader import aocinput
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt


def flat_hail_intersections(data: list[str], low_limit: int, high_limit: int) -> int:
    hails = []
    for line in data:
        parts = line.split('@')
        x, y, z = [float(part) for part in parts[0].split(',')]
        vx, vy, vz = [float(part) for part in parts[1].split(',')]

        a = vy / vx
        b = y - (a * x)
        hails.append((x, y, vx, vy, a, b))

    count = 0
    for hail_a, hail_b in combinations(hails, 2):
        x1, y1, vx1, vy1, a1, b1 = hail_a
        x2, y2, vx2, vy2, a2, b2 = hail_b

        if a1 == a2:  # same slope, wont intersect
            continue
        x_intersect = (b2 - b1) / (a1 - a2)
        y_intersect = a1 * x_intersect + b1

        if low_limit < x_intersect < high_limit and low_limit < y_intersect < high_limit:  # inside test area
            if (x_intersect - x1) * vx1 > 0 and (x_intersect - x2) * vx2 and (y_intersect - y1) * vy1 > 0 and (
                    y_intersect - y2) * vy2 > 0:  # intersection is "in future"
                count += 1
    return count


def stone_of_destruction(data: list[str]) -> int:
    positions = list()
    velocities = list()

    for line in data[:4]:
        parts = line.split('@')
        p = np.array([int(part) for part in parts[0].split(',')])
        v = np.array([int(part) for part in parts[1].split(',')])

        positions.append(p)
        velocities.append(v)

    guess_range = 220
    for dvx in range(0, guess_range):
        for dvy in range(0, guess_range):  # find intersection in xy plane
            dv = np.array([dvx, dvy, 0])
            if xy_intersect(dv, positions, velocities):
                for dvz in range(0, guess_range):  # then check it in z plane
                    dv[2] = dvz
                    if result := xyz_intersection(dv, positions, velocities):
                        return result


def xy_intersect(dv: np.ndarray, positions: list[np.ndarray], velocities: list[np.ndarray]) -> bool:
    p_intersect = None
    for info1, info2 in combinations(zip(positions, velocities), 2):
        p1, v1 = info1
        p2, v2 = info2
        v1 = v1 - dv
        v2 = v2 - dv
        if v1[0] == 0 or v2[0] == 0:
            continue

        a1 = v1[1] / v1[0]
        b1 = p1[1] - (a1 * p1[0])

        a2 = v2[1] / v2[0]
        b2 = p2[1] - (a2 * p2[0])

        if a1 == a2:
            continue

        x_intersect = (b2 - b1) / (a1 - a2)
        y_intersect = a1 * x_intersect + b1
        p_intersect_temp = (int(x_intersect), int(y_intersect))
        if p_intersect is None:
            p_intersect = p_intersect_temp
            continue
        if p_intersect_temp != p_intersect:
            return False
    return True


def xyz_intersection(dv: np.ndarray, positions: list[np.ndarray], velocities: list[np.ndarray]) -> int:

    for info1, info2 in combinations(zip(positions, velocities), 2):
        p1, v1 = info1
        p2, v2 = info2
        v1 = v1 - dv
        v2 = v2 - dv
        if v1[0] == 0 or v2[0] == 0:
            continue

        a1 = v1[1] / v1[0]
        b1 = p1[1] - (a1 * p1[0])

        a2 = v2[1] / v2[0]
        b2 = p2[1] - (a2 * p2[0])

        if a1 == a2:
            continue

        x_intersect = (b2 - b1) / (a1 - a2)
        y_intersect = a1 * x_intersect + b1
        t1 = (x_intersect - p1[0]) / v1[0]
        t2 = (x_intersect - p2[0]) / v2[0]
        z1 = int(p1[2] + v1[2] * t1)  #
        z2 = int(p2[2] + v2[2] * t2)
        if not z1 == z2:
            return False
    return int(x_intersect + y_intersect + z1)


def main(day: int):
    data = aocinput(day)
    results = flat_hail_intersections(data, 200000000000000, 400000000000000)
    results2 = stone_of_destruction(data)
    print(results, results2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
