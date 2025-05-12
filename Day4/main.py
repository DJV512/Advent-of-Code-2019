FILENAME = "sample_input.txt"
#FILENAME = "input.txt"

import time
import utils


def main():
    start_time = time.time()

    parse_time = time.time()

    answer1 = part1()
    part1_time = time.time()
    answer2 = part2()
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


def part1():

    total = 0
    for i in range(382345, 843168):
        x = list(str(i))
        double = False
        bad = False
        for j in range(1, len(x)):
            if x[j] < x[j-1]:
                bad = True
                break
            if x[j] == x[j-1]:
                double = True
        if not bad and double:
            total += 1

    return total


def part2():
    total = 0
    for i in range(382345, 843168):
        x = list(str(i))
        double = False
        triple = False
        bad = False
        double_digits = set()
        triple_digits = set()
        for j in range(1, len(x)):
            if x[j] < x[j-1]:
                bad = True
                break
            if x[j] == x[j-1]:
                double = True
                double_digits.add(x[j])
            try:
                if x[j] == x[j-1] and x[j] == x[j-2]:
                    triple = True
                    triple_digits.add(x[j])
            except IndexError:
                pass
        if not bad and double:
            if triple:
                if len(double_digits) > len(triple_digits):
                    total += 1
            else:
                total += 1
    
    return total


if __name__ == "__main__":
    main()