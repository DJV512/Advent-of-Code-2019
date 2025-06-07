# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from collections import defaultdict, deque


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

    coords = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line.strip("\n")):
            coords[(y,x)] = char
    return coords


def part1(data):

    max_y = max(y for y,x in data.keys())
    max_x = max(x for y,x in data.keys())

    portals = defaultdict(list)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if 65 <= ord(data[(y,x)]) <= 90:
                if y+1 <= max_y and 65 <= ord(data[(y+1,x)]) <= 90:
                    if y-1 >= 0 and data[(y-1,x)] == ".":
                        portals[f"{data[(y,x)]}{data[(y+1, x)]}"].append((y-1, x))
                    else:
                        portals[f"{data[(y,x)]}{data[(y+1, x)]}"].append((y+2, x))
                elif x+1 <= max_x and 65 <= ord(data[(y,x+1)]) <= 90:
                    if x-1 >= 0 and data[(y, x-1)] == ".":
                        portals[f"{data[(y,x)]}{data[(y, x+1)]}"].append((y, x-1))
                    else:
                        portals[f"{data[(y,x)]}{data[(y, x+1)]}"].append((y, x+2))

    warps = {}
    for portal in portals:
        if portal == "AA":
            start = portals[portal][0]
        elif portal == "ZZ":
            end = portals[portal][0]
        else:
            point1, point2 = portals[portal]
            warps[point1] = point2
            warps[point2] = point1

    maze_x_min = 2
    maze_x_max = max_x - 2
    maze_y_min = 2
    maze_y_max = max_y - 2


    queue = deque()
    queue.append((0, start))
    visited = set()

    while queue:
        steps, position = queue.popleft()

        if position == end:
            return steps
    
        visited.add(position)

        for direction in utils.DIRS_4:
            next_position = (position[0] + direction[0], position[1] + direction[1])

            if next_position not in visited and maze_y_min <= next_position[0] <= maze_y_max and maze_x_min <= next_position[1] <= maze_x_max and data[next_position] == ".":
                    queue.append((steps+1, next_position))
        
        if position in warps and warps[position] not in visited:
            queue.append((steps + 1, warps[position]))


def part2(data):

    max_y = max(y for y,x in data.keys())
    max_x = max(x for y,x in data.keys())

    maze_x_min = 2
    maze_x_max = max_x - 2
    maze_y_min = 2
    maze_y_max = max_y - 2

    portals = defaultdict(list)
    for y in range(max_y + 1):

        if y < maze_y_min or y > maze_y_max:
            y_location = -1
        else:
            y_location = 1

        for x in range(max_x + 1):

            if x < maze_x_min or x > maze_x_max:
                x_location = -1
            else:
                x_location = 1

            if 65 <= ord(data[(y,x)]) <= 90:
                if y+1 <= max_y and 65 <= ord(data[(y+1,x)]) <= 90:
                    if y-1 >= 0 and data[(y-1,x)] == ".":
                        portals[f"{data[(y,x)]}{data[(y+1, x)]}"].append(((y-1, x), y_location))
                    else:
                        portals[f"{data[(y,x)]}{data[(y+1, x)]}"].append(((y+2, x), y_location))
                elif x+1 <= max_x and 65 <= ord(data[(y,x+1)]) <= 90:
                    if x-1 >= 0 and data[(y, x-1)] == ".":
                        portals[f"{data[(y,x)]}{data[(y, x+1)]}"].append(((y, x-1), x_location))
                    else:
                        portals[f"{data[(y,x)]}{data[(y, x+1)]}"].append(((y, x+2), x_location))

    warps = {}
    for portal in portals:
        if portal == "AA":
            start = portals[portal][0][0]
        elif portal == "ZZ":
            end = portals[portal][0][0]
        else:
            (point1, level1), (point2, level2) = portals[portal]
            warps[point1] = (point2, level1)
            warps[point2] = (point1, level2)

    queue = deque()
    queue.append((0, start, 0))
    visited = set()

    while queue:
        steps, position, level = queue.popleft()

        if position == end and level == 0:
            return steps
    
        visited.add((position, level))

        for direction in utils.DIRS_4:
            next_position = (position[0] + direction[0], position[1] + direction[1])

            if (next_position, level) not in visited and maze_y_min <= next_position[0] <= maze_y_max and maze_x_min <= next_position[1] <= maze_x_max and data[next_position] == ".":
                    queue.append((steps+1, next_position, level))
        
        if position in warps and level + warps[position][1] >= 0 and (warps[position][0], level + warps[position][1]) not in visited:
            queue.append((steps + 1, warps[position][0], level + warps[position][1]))


if __name__ == "__main__":
    main()