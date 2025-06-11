import time
import utils
from collections import deque
import re


def main():
    start_time = time.time()

    data = parse_data()
    parse_time = time.time()

    answer1 = part1(data)
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


def parse_data():
    # FILENAME = "sample_input.txt"
    FILENAME = "input.txt"
    return utils.parse_input(FILENAME, method="raw")


def increment(deck, skip):
    deck = list(deck)
    length = len(deck)
    new_deck = ["." for _ in range(length)]
    for i, x in enumerate(range(0, length*skip, skip)):
        new_deck[x%length] = deck[i]
    return deque(new_deck)


def cut(deck, shift):
    deck.rotate(-shift)
    return deck


def stack(deck):
    return deque(reversed(deck))


def part1(data):

    deck = deque(range(10007))
    for line in data:
        if "increment" in line:
            pattern = r"\d+"
            skip = int(re.findall(pattern, line)[0])
            deck = increment(deck, skip)
        elif "cut" in line:
            pattern = r"-?\d+"
            shift = int(re.findall(pattern, line)[0])
            deck = cut(deck, shift)
        elif "stack" in line:
            deck = stack(deck)

    return list(deck).index(2019)


def part2():

    ## You can see by my part1 code above that it would NEVER have finished part2.
    ## Many thanks to metalim for this code - I had no clue how to figure out this math for myself
    ## https://github.com/metalim/adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb

    with open('input.txt') as file:
        input = file.read()

    rules = input.split('\n')
     
    def parse(L, rules):
        a,b = 1,0
        for s in rules[::-1]:
            if s.startswith('deal into new stack'):
                a = -a
                b = L-b-1
                continue
            if s.startswith('cut'):
                n = int(s.split(' ')[1])
                b = (b+n)%L
                continue
            if s.startswith('deal with increment'):
                n = int(s.split(' ')[3])
                z = pow(n,L-2,L) # == modinv(n,L)
                a = a*z % L
                b = b*z % L
                continue
            raise Exception('unknown rule', s)
        return a,b

    # modpow the polynomial: (ax+b)^m % n
    # f(x) = ax+b
    # g(x) = cx+d
    # f^2(x) = a(ax+b)+b = aax + ab+b
    # f(g(x)) = a(cx+d)+b = acx + ad+b
    def polypow(a,b,m,n):
        if m==0:
            return 1,0
        if m%2==0:
            return polypow(a*a%n, (a*b+b)%n, m//2, n)
        else:
            c,d = polypow(a,b,m-1,n)
            return a*c%n, (a*d+b)%n

    def shuffle2(L, N, pos, rules):
        a,b = parse(L,rules)
        a,b = polypow(a,b,N,L)
        return (pos*a+b)%L
    
    L = 119315717514047
    N = 101741582076661
    return shuffle2(L,N,2020,rules)


        


if __name__ == "__main__":
    main()