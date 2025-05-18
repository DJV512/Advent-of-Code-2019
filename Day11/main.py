# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict
from y2019.intcode import Intcode
from copy import deepcopy


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    part2data = deepcopy(data)

    answer1 = part1(data)
    part1_time = time.time()
    answer2 = part2(part2data)
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

    codes = defaultdict(int)
    for i,x in enumerate(data.strip().split(",")):
        codes[i] = int(x)

    return codes


def part1(data):
    panels = defaultdict(int)
    location = (0,0)
    direction = (-1, 0)
    painted = set()

    robot = Intcode(data)
    runner = robot.run()
    next(runner)

    while True:
        try:
            robot.inputs.append(panels[location])
            color = next(runner)
            dir = next(runner)
            if color == 0:
                panels[location] = 0
                painted.add(location)
            elif color == 1:
                panels[location] = 1
                painted.add(location)

            if dir == 0:
                if direction == (-1,0):
                    direction = (0,-1)
                elif direction == (0, 1):
                    direction = (-1, 0)
                elif direction == (1, 0):
                    direction = (0, 1)
                elif direction == (0, -1):
                    direction = (1, 0)
            elif dir == 1:
                if direction == (-1,0):
                    direction = (0,1)
                elif direction == (0, 1):
                    direction = (1, 0)
                elif direction == (1, 0):
                    direction = (0, -1)
                elif direction == (0, -1):
                    direction = (-1, 0)

            location = (location[0] + direction[0], location[1] + direction[1])
        
        except StopIteration:
            return len(painted)
    


def part2(data):
    panels = defaultdict(int)
    location = (0,0)
    direction = (-1, 0)
    painted = set()
    panels[location] = 1

    robot = Intcode(data)
    runner = robot.run()
    next(runner)
    
    while True:
        try:
            robot.inputs.append(panels[location])
            color = next(runner)
            dir = next(runner)
            if color == 0:
                panels[location] = 0
                painted.add(location)
            elif color == 1:    
                panels[location] = 1
                painted.add(location)

            if dir == 0:
                if direction == (-1,0):
                    direction = (0,-1)
                elif direction == (0, 1):
                    direction = (-1, 0)
                elif direction == (1, 0):
                    direction = (0, 1)
                elif direction == (0, -1):
                    direction = (1, 0)
            elif dir == 1:
                if direction == (-1,0):
                    direction = (0,1)
                elif direction == (0, 1):
                    direction = (1, 0)
                elif direction == (1, 0):
                    direction = (0, -1)
                elif direction == (0, -1):
                    direction = (-1, 0)

            location = (location[0] + direction[0], location[1] + direction[1])
        
        except StopIteration:
            break

    max_y = max(y for y,x in panels.keys())+1
    max_x = max(x for y,x in panels.keys())+1
    min_y = min(y for y,x in panels.keys())
    min_x = min(x for y,x in panels.keys())
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if panels[(y,x)] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


if __name__ == "__main__":
    main()