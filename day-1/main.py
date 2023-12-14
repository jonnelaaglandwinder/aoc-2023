import re
import sys

def convert(s):
  alpha = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

  try:
    return str(alpha.index(s) + 1)
  except:
    return s

def main():
  lines = [x for x in sys.stdin.readlines() if x != '\n']

  matches = [re.finditer(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line) for line in lines]
  matches = [
    [x.group(1) for x in match]
    for match in matches
  ]

  matches = map(lambda x: int(convert(x[0]) + convert(x[-1])), matches)

  print('sum of calibration values:', sum(matches))

if __name__ == '__main__':
  main()