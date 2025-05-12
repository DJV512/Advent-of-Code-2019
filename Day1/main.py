# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data)
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

    return data


def fuel_needed(mass):
    return mass//3 -2 


def part1(data):
    total = 0
    for line in data:
        a = int(line.strip())
        total += fuel_needed(a)

    return total


def part2(data):
    total = 0
    for line in data:
        a = int(line.strip())
        fuel = fuel_needed(a)
        total += fuel
        new_fuel = fuel_needed(fuel)
        while new_fuel > 0:
            total += new_fuel
            new_fuel = fuel_needed(new_fuel)

    return total


if __name__ == "__main__":
    main()
