import time
import utils
from y2019.intcode import Intcode
from math import inf


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
    # FILENAME = "sample_input.txt"
    FILENAME = "input.txt"
    return utils.parse_input(FILENAME, method="intcode")


def part1(data):

    network = []
    for i in range(50):
        computer = Intcode(data)
        computer.inputs.append(i)
        runner = computer.run()
        next(runner)
        network.append((computer, runner))
    
    while True:
        for x, (computer, runner) in enumerate(network):
            if not computer.inputs:
                computer.inputs.append(-1)

            destination = next(runner)
            if destination != "waiting":
                x = next(runner)
                y = next(runner)

                if destination == 255:
                    return y
                else:
                    network[destination][0].inputs.append(x)
                    network[destination][0].inputs.append(y)



def part2(data):

    network = []
    for i in range(50):
        computer = Intcode(data)
        computer.inputs.append(i)
        runner = computer.run()
        next(runner)
        network.append((computer, runner))
    
    last_y = float(inf)

    while True:
        no_inputs = []
        for x, (computer, runner) in enumerate(network):
            if not computer.inputs:
                no_inputs.append(True)
                computer.inputs.append(-1)
            else:
                no_inputs.append(False)

            destination = next(runner)
            if destination != "waiting":
                x = next(runner)
                y = next(runner)

                if destination == 255:
                    NAT = (x,y)
                else:
                    network[destination][0].inputs.append(x)
                    network[destination][0].inputs.append(y)

        if all(no_inputs):
            if NAT[1] == last_y:
                return last_y
            else:
                last_y = NAT[1]

            network[0][0].inputs.append(NAT[0])
            network[0][0].inputs.append(NAT[1])

if __name__ == "__main__":
    main()