import sys
import re
from dataclasses import dataclass
from functools import cached_property

@dataclass
class Element():
  x: int
  y: int
  width: int
  number: int

@dataclass
class Symbol():
  x: int
  y: int
  sym: str

@dataclass
class Gear():
  x: int
  y: int
  part1: Element
  part2: Element

  @property
  def ratio(self):
    return self.part1.number * self.part2.number

class Board():
  def __init__(self, lines: list[str]):
    self.width = len(lines[0])
    self.height = len(lines)
    self.lines = lines

    self.elements = []
    self.symbols = []

    self.from_lines(lines)

  def adjacent_symbols(self, element: Element) -> list[Symbol]:
    bbx1 = element.x - 1
    bby1 = element.y - 1
    bbx2 = element.x + element.width
    bby2 = element.y + 1

    return [sym for sym in self.symbols if sym.x >= bbx1 and sym.x <= bbx2 and sym.y >= bby1 and sym.y <= bby2]

  def adjacent_elements(self, symbol: Symbol) -> list[Element]:
    def intersect(element: Element, symbol: Symbol) -> bool:
      bbx1 = element.x - 1
      bby1 = element.y - 1
      bbx2 = element.x + element.width
      bby2 = element.y + 1

      return symbol.x >= bbx1 and symbol.x <= bbx2 and symbol.y >= bby1 and symbol.y <= bby2

    return [element for element in self.elements if intersect(element, symbol)]

  @cached_property
  def gears(self):
    candidates = [s for s in self.symbols if s.sym == '*']
    gears = []

    for sym in candidates:
      adjacent = self.adjacent_elements(sym)

      if len(adjacent) == 2:
        gears.append(Gear(sym.x, sym.y, adjacent[0], adjacent[1]))

    return gears

  def print_board(self):
    for y, line in enumerate(self.lines):
      part_bounds = [[part.x, part.x+part.width] for part in self.parts if part.y == y]
      gear_parts = [gear.part1 for gear in self.gears if gear.part1.y == y] + [gear.part2 for gear in self.gears if gear.part2.y == y]
      gear_part_bounds = [[part.x, part.x+part.width] for part in gear_parts]

      for x, char in enumerate(line):
        if any([bound[0] == x for bound in part_bounds]):
          print('\033[94m', end='')
        if any([bound[0] == x for bound in gear_part_bounds]):
          print('\033[92m', end='')
        if any([bound[1] == x for bound in part_bounds]):
          print('\033[0m', end='')
        print(char, end='')

    print()

  @cached_property
  def parts(self):
    return [element for element in self.elements if len(self.adjacent_symbols(element)) > 0]

  def from_lines(self, lines: list[str]):
    for y, line in enumerate(lines):
      elements = re.finditer(r'\d+', line)
      symbols = re.finditer(r'[^\.\d\s]', line)

      for x in elements:
        self.elements.append(Element(x.start(), y, len(x.group(0)), int(x.group(0))))

      for x in symbols:
        self.symbols.append(Symbol(x.start(), y, x.group(0)))

def main():
  lines = [x for x in sys.stdin.readlines() if x != '\n']

  board = Board(lines)
  board.print_board()

  print('sum of parts: ', sum([part.number for part in board.parts]))
  print('sum of gears: ', sum([gear.ratio for gear in board.gears]))

if __name__ == '__main__':
  main()