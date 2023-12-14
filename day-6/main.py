import re, sys
import math
from functools import reduce
from sympy import solve, Symbol

distance_eq = lambda t, d: (t - d) * d

def winning_times(t, d):
    x = Symbol('x')
    
    x1, x2 = solve(distance_eq(t, x) - d - 1, x)

    return range(math.ceil(x1), math.floor(x2)+1)

def main():
    lines = sys.stdin.readlines()

    time = list(map(int, re.findall(r"\d+", lines[0])))
    distance = list(map(int, re.findall(r"\d+", lines[1])))

    times = [winning_times(t, d) for t, d in zip(time, distance)]
    num_times = list(map(len, times))

    print('phase1 result:', reduce(lambda x, y: x * y, num_times, 1), '({})'.format(' * '.join(map(str, num_times))))

    time_merged = int(''.join(re.findall(r"\d+", lines[0])))
    distance_merged = int(''.join(re.findall(r"\d+", lines[1])))

    print('phase2 result:', len(winning_times(time_merged, distance_merged)), 'possible winning times')


if __name__ == '__main__':
    main()