import sys
from functools import reduce

def rotate_cw(board: list[str]):
    return [''.join(reversed(list(x))) for x in zip(*board)]

def rotate_ccw(board: list[str]):
    return list(reversed([''.join(list(x)) for x in zip(*board)]))

def eval(board: list[str]):
    return ['#'.join([''.join(sorted(x)) for x in line.split('#')]) for line in board]

def run_cycle(board: list[str]):
    return reduce(lambda x, _: rotate_cw(eval(x)), range(4), board)

def print_board(board: list[str]):
    print('\n'.join(board))

def load(board: list[str]):
    return sum([len(board)-y for y, line in enumerate(board) for c in line if c == 'O'])

class HashableList(list):
    def __hash__(self) -> int:
        return sum([i * hash(x) for i, x in enumerate(self)])

def main():
    board = [line.strip() for line in sys.stdin.readlines()]
    board = rotate_cw(board)

    boards = [HashableList(board)]
    seen = set(boards)

    iter = 0
    while True:
        iter += 1

        board = run_cycle(board)

        if HashableList(board) in seen:
            break

        if iter % 1000 == 0:
            print(iter)

        seen.add(HashableList(board))
        boards.append(HashableList(board))

    first = boards.index(HashableList(board))

    billionth_idx = (1000000000 - first) % (iter - first) + first
    billionth = rotate_ccw(boards[billionth_idx])

    print('load after 1 000 000 000 cycles: {}'.format(load(billionth)))

if __name__ == '__main__':
    main()