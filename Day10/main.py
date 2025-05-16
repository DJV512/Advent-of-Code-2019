# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
import math
from collections import defaultdict


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1, asteroids, location = part1(data)
    part1_time = time.time()
    answer2 = part2(asteroids, location)
    part2_time = time.time()

    print("---------------------------------------------------")
    print(f"Part 1 Answer: {answer1}")
    print()
    print(f"Part 2 Answer: {answer2}")
    print()
    print(f"Data Parse Execution Time: {1000*(parse_time - start_time):.2f} ms")
    print(f"Part 1 Execution Time:     {1000*(part1_time - parse_time):.2f} ms")
    print(f"Part 2 Execution Time:     {1000*(part2_time - part1_time):.2f} ms")
    print(f"Total Execution Time:      {1000*(part2_time - start_time):.2f} ms")
    print("---------------------------------------------------")


output = True  # Toggle this flag to enable/disable prints
def debug_print(*args, **kwargs):
    if output:
        print(*args, **kwargs)


def parse_data():
    with open(FILENAME, "r") as f:
        data = f.readlines()

    return utils.grid_parse_dict(data)


def part1(data):

    asteroids = set()

    length = max(data, key = lambda y: y[0])[0]
    width = max(data, key = lambda x: x[1])[1]

    for y in range(length+1):
        for x in range(width+1):
            if data[(y,x)] == "#":
                asteroids.add((y,x))
    
    catalog = {}
    for asteroid1 in asteroids:
        total = 0
        for asteroid2 in asteroids:
            if asteroid1 != asteroid2:
                ychange = asteroid2[0]-asteroid1[0]
                xchange = asteroid2[1]-asteroid1[1]
                gcd = math.gcd(ychange, xchange)
                if gcd != 1:
                    ychange /= gcd
                    xchange /= gcd
                y = asteroid1[0]
                x = asteroid1[1]
                while 0 <= y <= length and 0 <= width <= width:
                    y += ychange
                    x += xchange

                    if (y,x) in asteroids and (y,x) != asteroid2:
                        break
                    elif (y,x) == asteroid2:
                        total += 1
                        break
        catalog[asteroid1] = total
    
    most_seen = max(catalog.values())

    for key in catalog:
        if catalog[key] == most_seen:
            location = key
            break
                    
    return most_seen, asteroids, location


def part2(asteroids, location):

    targets = defaultdict(list)
    for asteroid in asteroids:
        if asteroid != location:
            ychange = asteroid[0] - location[0]
            xchange = asteroid[1] - location[1]
            angle = math.degrees(math.atan2(ychange, xchange))+90
            targets[angle].append(asteroid)

    for key in targets.copy():
        targets[key] = sorted(targets[key], key=lambda x: utils.manhattan(x, location))
        if key < 0:
            targets[key + 360] = targets[key]
            targets.pop(key)

    angles = list(sorted(targets))

    i = 0
    killed = []
    while len(asteroids) > 1:
        asteroid = targets[angles[i%len(angles)]]
        if len(asteroid) > 0:
            lasered = asteroid.pop(0)
            asteroids.remove(lasered)
            killed.append(lasered)
        i += 1

    return killed[199][1] * 100 + killed[199][0]


if __name__ == "__main__":
    main()