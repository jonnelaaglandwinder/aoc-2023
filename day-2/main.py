import re
import sys
from dataclasses import dataclass

@dataclass
class Draw():
  color: str
  count: int

  def __repr__(self) -> str:
    return f'{self.count} {self.color}'

class Round():
  @property
  def red(self):
    return sum([draw.count for draw in self.draws if draw.color == 'red'])

  @property
  def green(self):
    return sum([draw.count for draw in self.draws if draw.color == 'green'])
  
  @property
  def blue(self):
    return sum([draw.count for draw in self.draws if draw.color == 'blue'])

  def valid(self):
    return self.red <= 12 and self.green <= 13 and self.blue <= 14


  def __init__(self, draws: list[Draw]):
    self.draws = draws

  def __repr__(self) -> str:
    return ';'.join([str(x) for x in self.draws])

@dataclass
class Game():
  id: str
  rounds: list[Round]

  @property
  def red(self):
    return sum([round.red for round in self.rounds])

  @property
  def green(self):
    return sum([round.green for round in self.rounds])
  
  @property
  def blue(self):
    return sum([round.blue for round in self.rounds])

  @property
  def power(self):
    red = max([round.red for round in self.rounds])
    green = max([round.green for round in self.rounds])
    blue = max([round.blue for round in self.rounds])

    return red * green * blue

  def valid(self):
    return all([round.valid() for round in self.rounds])

  def __repr__(self) -> str:
    return '#{}, {} red, {} green, {} blue'.format(self.id, self.red, self.green, self.blue)

def parse_rounds(s: str):
  rounds = s.split(';')

  def parse_draw(s: str):
    match = re.match(r'\s*(\d+) (red|green|blue)\s*', s)
    return Draw(match.group(2), int(match.group(1)))

  return [Round([parse_draw(draw) for draw in round.split(',')]) for round in rounds]

def parse_game(s):
  match = re.match(r'Game (\d+): (.*)', s)

  return Game(
    id=int(match.group(1)),
    rounds=parse_rounds(match.group(2))
  )

def main():
  games = [parse_game(x) for x in sys.stdin.readlines() if x != '\n']
  valid_games = [game for game in games if game.valid()]

  print('sum of valid games: ', sum([game.id for game in valid_games]))
  print('total power of all games', sum([game.power for game in games]))

if __name__ == '__main__':
  main()