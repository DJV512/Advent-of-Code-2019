# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from y2019.intcode import Intcode
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
        data = f.read()

    memory = defaultdict(int)
    for i, item in enumerate(data.strip().split(",")):
        memory[i] = int(item)

    return memory


def part1(data):

    robot = Intcode(data)
    runner = robot.run()
    map = {}
    location = (0,0)
    while True:
        try:
            output = next(runner)
            if output == 10:
                location = (location[0]+1, 0)
            else:
                map[location] = chr(output)
                location = (location[0], location[1]+1)
        except StopIteration:
            break

    intersections = set()
    max_y = max(y for y,x in map)
    max_x = max(x for y,x in map)

    for key in map:
        if map[key] == "#":
            if all((key[0] > 0, key[0] < max_y, key[1] > 0, key[1] < max_x)):
                if all((map[(key[0]+1, key[1])] == "#", map[(key[0]-1, key[1])] == "#", map[(key[0], key[1]+1)] == "#", map[(key[0], key[1]-1)] == "#")):
                    intersections.add(key)
    
    total = 0
    for intersection in intersections:
        total += intersection[0]*intersection[1]

    return total


def part2(data):
    robot = Intcode(data)
    robot.memory[0] = 2
    runner = robot.run()
    inputs = "A,B,B,A,B,C,A,C,B,C\nL,4,L,6,L,8,L,6,6\nL,8,R,6,6,L,6,6\nR,6,6,L,6,L,6,L,8\nn\n"
    for x in inputs:
        robot.inputs.append(ord(x))

    map = {}
    location = (0,0)

    while True:
        try:
            output = next(runner)
            if output == 10:
                if flag:
                    time.sleep(0.01)
                    print(utils.CLEAR)
                    utils.print_grid_dict(map)
                    flag = False
                    location = (0,0)
                else:
                    location = (location[0]+1, 0)
                    flag = True
            else:
                map[location] = chr(output)
                location = (location[0], location[1]+1)
                flag = False
        except StopIteration:
            break

    return output


if __name__ == "__main__":
    main()