# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from y2019.intcode import Intcode
from copy import deepcopy


def main():
    start_time = time.time()

    data = parse_data()
    part2data = deepcopy(data)
    parse_time = time.time()

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

    return {i:int(x) for i, x in enumerate(data.strip().split(","))}


def part1(data):

    screen = {}

    game = Intcode(data)
    runner = game.run()
    
    while True:
        try:
            x = next(runner)
            y = next(runner)
            id = next(runner)

            screen[(y,x)] = id
        except StopIteration:
            break

    count = 0
    for key in screen:
        if screen[key] == 2:
            count += 1

    return count


def part2(data):
    screen = {}

    game = Intcode(data)
    game.memory[0] = 2
    runner = game.run()
    score = 0
    
    while True:
        x = next(runner)
        y = next(runner)

        if x == "waiting" or y == "waiting":
            break
        
        if x == -1 and y == 0:
            score = next(runner)
        else:
            id = next(runner)
            screen[(y,x)] = id
                
    min_y = min(y for y,x in screen.keys())
    max_y = max(y for y,x in screen.keys())
    min_x = min(x for y,x in screen.keys())
    max_x = max(x for y,x in screen.keys())
     
    while True:
        try:
            x = None
            y = None
            id = None

            # print(utils.CLEAR)    
            # print(f"Score = {score}")
            # for y in range(min_y, max_y+1):
            #     for x in range(min_x, max_x+1):
            #         if (y,x) not in screen:
            #             continue
            #         elif screen[(y,x)] == 0:
            #             print(" ", end="")
            #         elif screen[(y,x)] == 1:
            #             print("W", end="")
            #         elif screen[(y,x)] == 2:
            #             print("#", end="")
            #         elif screen[(y,x)] == 3:
            #             print("-", end="")
            #         elif screen[(y,x)] == 4:
            #             print("o", end="")
            #     print()
            
            ball = False
            paddle = False
            for key in screen:
                if screen[key] == 4:
                    ballx = key[1]
                    ball = True
                elif screen[key] == 3:
                    paddlex = key[1]
                    paddle = True
                
                if ball and paddle:
                    break

            if ballx > paddlex:
                game.inputs.append(1)
            elif ballx < paddlex:
                game.inputs.append(-1)
            elif ballx == paddlex:
                game.inputs.append(0)

            while x != "waiting":
                x = next(runner)
                y = next(runner)
                if x == -1 and y == 0:
                    score = next(runner)
                else:
                    id = next(runner)
                    screen[(y,x)] = id

        except StopIteration:
            break

    return score


if __name__ == "__main__":
    main()