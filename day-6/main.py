import re, sys
from math import ceil, floor, prod
from functools import reduce
from sympy import solve, Symbol

def winning_times(race_duration, distance_to_beat):
    x = Symbol('x')
    
    x1, x2 = solve((race_duration - x) * x - distance_to_beat, x)

    return range(ceil(x1), floor(x2)+1)

def main():
    lines = sys.stdin.readlines()

    time = list(map(int, re.findall(r"\d+", lines[0])))
    distance = list(map(int, re.findall(r"\d+", lines[1])))

    times = [winning_times(t, d) for t, d in zip(time, distance)]
    num_times = list(map(len, times))

    print('phase1 result:', prod(num_times), '({})'.format(' * '.join(map(str, num_times))))

    time_merged = int(''.join(re.findall(r"\d+", lines[0])))
    distance_merged = int(''.join(re.findall(r"\d+", lines[1])))

    print('phase2 result:', len(winning_times(time_merged, distance_merged)), 'possible winning times')


if __name__ == '__main__':
    main()