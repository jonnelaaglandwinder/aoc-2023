import re, sys
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    my_numbers: list[int]

    @property
    def match_count(self):
        return len([
            n for n in self.my_numbers if n in self.winning_numbers
        ])

    @property
    def value(self):
        count = self.match_count

        return (1 * 2 ** (count - 1)) if count > 0 else 0

    def parse(s: str):
        match = re.match(r"Card\s+(\d+): (.+) \| (.+)", s)

        if match:
            id = int(match.group(1))
            winning_numbers = list(map(int, map(lambda x: x.group(0), re.finditer(r'\d+', match.group(2)))))
            my_numbers = list(map(int, map(lambda x: x.group(0), re.finditer(r'\d+', match.group(3)))))

            return Card(id, winning_numbers, my_numbers)
        else:
            raise Exception("Invalid card", s)

class CardSet:
    def __init__(self, card: Iterable[Card]) -> None:
        self.cards = list(card)
        pass

    def phase1_value(self):
        return sum(map(lambda c: c.value, self.cards))
    
    def phase2_value(self):
        copies = [1 for i in range(0, len(self.cards))]

        for i in range(len(self.cards)):
            for j in range(i + 1, min(len(self.cards), i + 1 + self.cards[i].match_count)):
                copies[j] += copies[i]

        return sum(copies)

    def parse(s: Iterable[str]):
        cards = map(Card.parse, s)

        return CardSet(cards)

def main():
    lines = sys.stdin.readlines()
    cardset = CardSet.parse(lines)

    print('phase 1 value:', cardset.phase1_value())
    print('phase 2 value:', cardset.phase2_value())

if __name__ == "__main__":
    main()