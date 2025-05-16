# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict
from y2019.intcode import Intcode


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
    
    memory = defaultdict(int)
    for i, item in enumerate(data.strip().split(",")):
        memory[i] = int(item)

    return memory


def part1(data):

    computer = Intcode(data, interactive=True)
    computer.run_without_halt()

    return computer.memory[64]


def part2(data):

    computer = Intcode(data, interactive=True)
    computer.run_without_halt()

    return computer.memory[1001]


if __name__ == "__main__":
    main()