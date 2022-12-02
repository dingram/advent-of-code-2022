#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


SHAPE_SCORES = {
    'X': 1,  # Rock
    'Y': 2,  # Paper
    'Z': 3,  # Scissors
}
OUTCOMES = {
    ('X', 'A'): 3,  # Rock     = Rock: Draw
    ('Y', 'A'): 6,  # Paper    > Rock: Win
    ('Z', 'A'): 0,  # Scissors < Rock: Lose

    ('X', 'B'): 0,  # Rock     < Paper: Lose
    ('Y', 'B'): 3,  # Paper    = Paper: Draw
    ('Z', 'B'): 6,  # Scissors > Paper: Win

    ('X', 'C'): 6,  # Rock     > Scissors: Win
    ('Y', 'C'): 0,  # Paper    < Scissors: Lose
    ('Z', 'C'): 3,  # Scissors = Scissors: Draw
}


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    total_score = 0
    for line in input_file:
      opponent_move, my_move = line.strip().split(' ')
      outcome = OUTCOMES[my_move, opponent_move]
      shape_score = SHAPE_SCORES[my_move]
      score = outcome + shape_score
      print(f'{opponent_move} vs {my_move} -> {outcome=} + {shape_score=} = {score=}')
      total_score += score
  print('Total score:', total_score)


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
