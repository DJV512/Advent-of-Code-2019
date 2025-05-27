# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from y2019.intcode import Intcode
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
        data = f.read()

    return {i:int(x) for i, x in enumerate(data.strip().split(","))}


def question():
    return "?"


def part1(data):

    droid = Intcode(data)
    runner = droid.run()
    next(runner)

    map = defaultdict(question)
    position = (0,0)
    map[position] = "."

    dead_ends = set()


    while True:
        # Check for dead ends so we don't get stuck in a loop
        count = 0
        for direction in utils.DIRS_4:
            new_position = (position[0]+direction[0],position[1]+direction[1])
            if map[new_position] == "#" or new_position in dead_ends:
                count += 1
        if count == 3:
            dead_ends.add(position)

        # Decide which input to send to the droid
        if map[(position[0]-1, position[1])] == "?":
            input = 1
            droid.inputs.append(input)
        elif map[(position[0]+1, position[1])] == "?":
            input = 2
            droid.inputs.append(input)
        elif map[(position[0], position[1]-1)] == "?":
            input = 3
            droid.inputs.append(input)
        elif map[(position[0], position[1]+1)] == "?":
            input = 4
            droid.inputs.append(input)
        elif map[(position[0]-1, position[1])] == "." and (position[0]-1, position[1]) not in dead_ends:
            input = 1
            droid.inputs.append(input)
        elif map[(position[0]+1, position[1])] == "." and (position[0]+1, position[1]) not in dead_ends:
            input = 2
            droid.inputs.append(input)
        elif map[(position[0], position[1]-1)] == "." and (position[0], position[1]-1) not in dead_ends:
            input = 3
            droid.inputs.append(input)
        elif map[(position[0], position[1]+1)] == "." and (position[0], position[1]+1) not in dead_ends:
            input = 4
            droid.inputs.append(input)

        # Receive feedback from the droid and update the map and position
        # Break if we've found the oxygen system
        output = next(runner)

        if output == 0:
            if input == 1:
                map[(position[0]-1, position[1])] = "#"
            elif input == 2:
                map[(position[0]+1, position[1])] = "#"
            elif input == 3:
                map[(position[0], position[1]-1)] = "#"
            elif input == 4:
                map[(position[0], position[1]+1)] = "#"
        elif output == 1:
            if input == 1:
                map[(position[0]-1, position[1])] = "."
                position = (position[0]-1, position[1])
            elif input == 2:
                map[(position[0]+1, position[1])] = "."
                position = (position[0]+1, position[1])
            elif input == 3:
                map[(position[0], position[1]-1)] = "."
                position = (position[0], position[1]-1)
            elif input == 4:
                map[(position[0], position[1]+1)] = "."
                position = (position[0], position[1]+1)
        elif output == 2:
            if input == 1:
                map[(position[0]-1, position[1])] = "X"
                position = (position[0]-1, position[1])
            elif input == 2:
                map[(position[0]+1, position[1])] = "X"
                position = (position[0]+1, position[1])
            elif input == 3:
                map[(position[0], position[1]-1)] = "X"
                position = (position[0], position[1]-1)
            elif input == 4:
                map[(position[0], position[1]+1)] = "X"
                position = (position[0], position[1]+1)
            break
    
    # Now that we know where the oxygen system is, we have to find the shortest path to get there
    # Perform a breadth first search from the starting (0,0) position to the goal
    # Once we find the goal, return the number of steps it took to get there
    goal = position
    queue = deque()
    queue.append(((0,0),0))
    visited = set()

    while queue:

        position, steps = queue.popleft()

        if position == goal:
            # utils.print_grid_dict(map)
            return steps
    
        visited.add(position)

        for direction in utils.DIRS_4:
            new_position = (position[0]+direction[0], position[1]+direction[1])
            if new_position not in visited:
                if map[new_position] not in ["#", "?"]:
                    queue.append((new_position, steps+1))


def part2(data):

    droid = Intcode(data)
    runner = droid.run()
    next(runner)

    map = defaultdict(question)
    position = (0,0)
    map[position] = "."

    queue = deque()
    queue.append((position, droid))

    visited = set()

    while queue:
        position, droid = queue.popleft()

        visited.add(position)

        for input in range(1, 5):
            if input == 1:
                direction = (-1, 0)
            elif input == 2:
                direction = (1, 0)
            elif input == 3:
                direction = (0, -1)
            elif input == 4:
                direction = (0, 1)
            

            new_position = (position[0]+direction[0],position[1]+direction[1])
            if map[new_position] != "#" and new_position not in visited:

                new_droid = droid.clone()
                new_runner = new_droid.run()
                new_droid.inputs.append(input)
                output = next(new_runner)

                if output == 0:
                    map[new_position] = "#"
                elif output in [1,2]:
                    map[new_position] = "."
                    if output == 2:
                        map[new_position] = "X"
                        oxygen = new_position
                    
                    queue.append((new_position, new_droid))

    queue = deque()
    queue.append((oxygen,0))
    visited = set()
    max_steps = 0

    while queue:

        position, steps = queue.popleft()

        max_steps = max(max_steps, steps)
    
        visited.add(position)

        for direction in utils.DIRS_4:
            new_position = (position[0]+direction[0], position[1]+direction[1])
            if new_position not in visited:
                if map[new_position] not in ["#", "?"]:
                    queue.append((new_position, steps+1))

    return max_steps


if __name__ == "__main__":
    main()