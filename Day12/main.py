FILENAME = "sample_input.txt"
#FILENAME = "input.txt"

import time
import utils
from copy import deepcopy
from math import lcm


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

    sample1 = {
        1: (-1,0,2,0,0,0),
        2: (2,-10,-7,0,0,0),
        3: (4,-8,8,0,0,0),
        4: (3,5,-1,0,0,0),
    }

    sample2 = {
        1: (-8,-10,0,0,0,0),
        2: (5,5,10,0,0,0),
        3: (2,-7,3,0,0,0),
        4: (9,-8,-3,0,0,0),
    }
    
    start = {
        1: (-16,15,-9,0,0,0),
        2: (-14,5,4,0,0,0),
        3: (2,0,6,0,0,0),
        4: (-3,18,9,0,0,0),
    }
    
    current = deepcopy(start)
    
    for i in range(1, 1001):
        new_current = {}
        for moon1 in current:
            x1, y1, z1, vx1, vy1, vz1 = current[moon1]
            for moon2 in current:
                x2, y2, z2, _, _, _ = current[moon2]
                if moon1 != moon2:
                    if x1 > x2:
                        vx1 -= 1
                    elif x2 > x1:
                        vx1 += 1
                    
                    if y1 > y2:
                        vy1 -= 1
                    elif y2 > y1:
                        vy1 += 1
                    
                    if z1 > z2:
                        vz1 -= 1
                    elif z2 > z1:
                        vz1 += 1
                    
            x1 += vx1
            y1 += vy1
            z1 += vz1
                    
            new_current[moon1] = (x1, y1, z1, vx1, vy1, vz1)

        current = new_current
    
        energy = 0
        for key in current:
            x, y, z, vx, vy, vz = current[key]
            energy += (abs(x)+abs(y)+abs(z))*(abs(vx)+abs(vy)+abs(vz))
    
    return energy


def flatten(moons):
    xstate = []
    ystate = []
    zstate = []
    for key in moons:
        a, b, c, d, e, f = moons[key]
        xstate.extend([a, d])
        ystate.extend([b, e])
        zstate.extend([c, f])
    return tuple(xstate), tuple(ystate), tuple(zstate)


def part2():

    sample1 = {
        1: (-1,0,2,0,0,0),
        2: (2,-10,-7,0,0,0),
        3: (4,-8,8,0,0,0),
        4: (3,5,-1,0,0,0),
    }

    sample2 = {
        1: (-8,-10,0,0,0,0),
        2: (5,5,10,0,0,0),
        3: (2,-7,3,0,0,0),
        4: (9,-8,-3,0,0,0),
    }
    
    start = {
        1: (-16,15,-9,0,0,0),
        2: (-14,5,4,0,0,0),
        3: (2,0,6,0,0,0),
        4: (-3,18,9,0,0,0),
    }
    
    current = deepcopy(start)

    xstates = set()
    ystates = set()
    zstates = set()
    xstate, ystate, zstate = flatten(current)
    xstates.add(xstate)
    ystates.add(ystate)
    zstates.add(zstate)
    i=0

    xfound = False
    yfound = False
    zfound = False


    while True:
        i+=1
        new_current = {}
        for moon1 in current:
            x1, y1, z1, vx1, vy1, vz1 = current[moon1]
            for moon2 in current:
                x2, y2, z2, _, _, _ = current[moon2]
                if moon1 != moon2:
                    if x1 > x2:
                        vx1 -= 1
                    elif x2 > x1:
                        vx1 += 1
                    
                    if y1 > y2:
                        vy1 -= 1
                    elif y2 > y1:
                        vy1 += 1
                    
                    if z1 > z2:
                        vz1 -= 1
                    elif z2 > z1:
                        vz1 += 1
                    
            x1 += vx1
            y1 += vy1
            z1 += vz1
                    
            new_current[moon1] = (x1, y1, z1, vx1, vy1, vz1)

        current = new_current
        xstate, ystate, zstate = flatten(current)
        if not xfound:
            if xstate in xstates:
                xstep = i
                xfound = True
            else:
                xstates.add(xstate)
        if not yfound:
            if ystate in ystates:
                ystep = i
                yfound = True
            else:
                ystates.add(ystate)
        if not zfound:
            if zstate in zstates:
                zstep = i
                zfound = True
            else:
                zstates.add(zstate)
        
        if xfound and yfound and zfound:
            break
    
    steps = lcm(xstep, ystep, zstep)

    return steps



if __name__ == "__main__":
    main()