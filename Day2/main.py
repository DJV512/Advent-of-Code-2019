# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from copy import deepcopy
from y2019.intcode import Intcode


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    data_copy = deepcopy(data)

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(data_copy)
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

    return [int(x) for x in data.strip().split(",")]


def part1(data):
    data[1] = 12
    data[2] = 2
    
    computer = Intcode(data)
    computer.run_without_halt()
    return computer.memory[0]


def part2(data_copy):

    for noun in range(100):
        for verb in range(100):
            temp = deepcopy(data_copy)
            temp[1] = noun
            temp[2] = verb
            computer = Intcode(temp)
            computer.run_without_halt()
            if computer.memory[0] == 19690720:
                return 100 * noun + verb

    return None


if __name__ == "__main__":
    main()