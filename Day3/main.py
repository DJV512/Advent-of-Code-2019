# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict

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

    wires = {}
    for i, line in enumerate(data):
        wires[i] = line.strip().split(",")

    return wires


def part1(wires):

    positions = defaultdict(set)
    start = (0,0)
    for z,key in enumerate(wires):
        current = start
        for instruction in wires[key]:
            direction = instruction[0]
            length = int(instruction[1:])
            for i in range(1, length+1):
                if direction == "R":
                    current = (current[0],current[1]+1)
                elif direction == "L":
                    current = (current[0],current[1]-1)
                elif direction == "U":
                    current = (current[0]-1,current[1])
                elif direction == "D":
                    current = (current[0]+1,current[1])
                positions[f"wire{z}"].add(current)
    
    common = positions["wire0"] & positions["wire1"]

    closest = 10000000000000000
    for point in common:
        distance = abs(point[0]) + abs(point[1])
        if distance < closest:
            closest = distance

    return closest


def part2(wires):
    positions = defaultdict(set)
    start = (0,0)
    for z,key in enumerate(wires):
        steps = 0
        current = start
        for instruction in wires[key]:
            direction = instruction[0]
            length = int(instruction[1:])
            for i in range(1, length+1):
                steps +=1
                if direction == "R":
                    current = (current[0],current[1]+1)
                elif direction == "L":
                    current = (current[0],current[1]-1)
                elif direction == "U":
                    current = (current[0]-1,current[1])
                elif direction == "D":
                    current = (current[0]+1,current[1])
                positions[f"wire{z}"].add((current,steps))

    wire0pos = {pos for pos,_ in positions["wire0"]}
    wire1pos = {pos for pos,_ in positions["wire1"]}

    common_positions = wire0pos & wire1pos
    
    wire0overlap = sorted([item for item in positions["wire0"] if item[0] in common_positions], key = lambda x: x[0])
    wire1overlap = sorted([item for item in positions["wire1"] if item[0] in common_positions], key = lambda x: x[0])

    fewest_steps = 100000000000
    for i in range(len(wire0overlap)):
        steps = wire0overlap[i][1] + wire1overlap[i][1]
        if steps < fewest_steps:
            fewest_steps = steps

    return fewest_steps



if __name__ == "__main__":
    main()