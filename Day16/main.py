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
        data = f.read()

    return [int(x) for x in list(data.strip())]


def part1(data):

    base = [0, 1, 0, -1]

    for _ in range(100):
        new_data = []

        for x in range(len(data)):
            new_base = [y for item in base for y in [item] * (x+1)]
            new_data.append(abs(sum(new_base[(j+1)%len(new_base)]*data[j] for j in range(len(data))))%10)
        data = new_data

    return "".join((str(x) for x in data[:8]))

def part2(data):

    start = int("".join(str(x) for x in data[:7]))
    data = (data*10000)[start:]

    for _ in range(100):
        suffix_sum = 0
        for i in reversed(range(len(data))):
            suffix_sum = (suffix_sum + data[i]) % 10
            data[i] = suffix_sum

    return "".join((str(x) for x in data[:8]))


if __name__ == "__main__":
    main()