# FILENAME = "sample_input.txt"
FILENAME = "input.txt"

import time
import utils
from y2019.intcode import Intcode
from itertools import permutations


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
    return [int(x) for x in data.strip().split(",")]


def part1(data):

    combos = permutations(range(5), 5)

    best_signal = 0
    for a,b,c,d,e in combos:

        amp_a = Intcode(data[:], [a, 0])
        amp_a.run_without_halt()

        amp_b = Intcode(data[:], [b, amp_a.outputs[0]])
        amp_b.run_without_halt()

        amp_c = Intcode(data[:], [c, amp_b.outputs[0]])
        amp_c.run_without_halt()

        amp_d = Intcode(data[:], [d, amp_c.outputs[0]])
        amp_d.run_without_halt()

        amp_e = Intcode(data[:], [e, amp_d.outputs[0]])
        amp_e.run_without_halt()

        best_signal = max(best_signal, amp_e.outputs[0])

    return best_signal


def part2(data):

    combos = permutations(range(5,10), 5)
    best_signal = 0

    for a,b,c,d,e in combos:
        amps = [Intcode(data[:], [phase]) for phase in [a,b,c,d,e]]

        runners = [amp.run() for amp in amps]

        for runner in runners:
            next(runner)
        
        signal = 0
        i = 0

        while not amps[-1].halted:
            amp = amps[i%5]
            runner = runners[i%5]
            amp.inputs.append(signal)

            try:
                signal = next(runner)
            except StopIteration:
                pass

            i += 1
    
        best_signal = max(best_signal, signal)

    return best_signal


if __name__ == "__main__":
    main()