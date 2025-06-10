# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
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
    return utils.parse_input(FILENAME, method="intcode")

def part1(data):

    droid = Intcode(data)
    runner = droid.run()
    while True:
        output = next(runner)
        if output not in [10, "waiting"]:
            print(chr(output), end="")
        elif output == 10:
            print()
        else:
            break
    instructions = "NOT A T\nNOT B J\nOR T J\nNOT C T\nOR T J\nAND D J\nWALK\n"
    # print(instructions)
    for char in instructions:
        droid.inputs.append(ord(char))
    
    while True:
        try:
            output = next(runner)
            if output != 10 and output < 200:
                print(chr(output), end="")
            elif output > 200:
                return output
            else:
                print()
        except StopIteration:
            break
 


def part2(data):

    droid = Intcode(data)
    runner = droid.run()
    while True:
        output = next(runner)
        if output not in [10, "waiting"]:
            print(chr(output), end="")
        elif output == 10:
            print()
        else:
            break
    instructions = "NOT A T\nNOT B J\nOR T J\nNOT C T\nOR T J\nAND D J\nNOT E T\nNOT T T\nOR H T\nAND T J\nRUN\n"
    # print(instructions)
    for char in instructions:
        droid.inputs.append(ord(char))
    
    while True:
        try:
            output = next(runner)
            if output != 10 and output < 200:
                print(chr(output), end="")
            elif output > 200:
                return output
            else:
                print()
        except StopIteration:
            break
    return None


if __name__ == "__main__":
    main()