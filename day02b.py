#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


SHAPE_SCORES = {
    'R': 1,  # Rock
    'P': 2,  # Paper
    'S': 3,  # Scissors
}
DESIRED_SHAPE = {
    ('X', 'A'): 'S',  # Lose against Rock
    ('Y', 'A'): 'R',  # Draw against Rock
    ('Z', 'A'): 'P',  # Win  against Rock

    ('X', 'B'): 'R',  # Lose against Paper
    ('Y', 'B'): 'P',  # Draw against Paper
    ('Z', 'B'): 'S',  # Win  against Paper

    ('X', 'C'): 'P',  # Lose against Scissors
    ('Y', 'C'): 'S',  # Draw against Scissors
    ('Z', 'C'): 'R',  # Win  against Scissors
}
OUTCOMES = {
    ('R', 'A'): 3,  # Rock     = Rock: Draw
    ('P', 'A'): 6,  # Paper    > Rock: Win
    ('S', 'A'): 0,  # Scissors < Rock: Lose

    ('R', 'B'): 0,  # Rock     < Paper: Lose
    ('P', 'B'): 3,  # Paper    = Paper: Draw
    ('S', 'B'): 6,  # Scissors > Paper: Win

    ('R', 'C'): 6,  # Rock     > Scissors: Win
    ('P', 'C'): 0,  # Paper    < Scissors: Lose
    ('S', 'C'): 3,  # Scissors = Scissors: Draw
}


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    total_score = 0
    for line in input_file:
      opponent_move, desired_outcome = line.strip().split(' ')
      my_move = DESIRED_SHAPE[desired_outcome, opponent_move]

      outcome = OUTCOMES[my_move, opponent_move]
      shape_score = SHAPE_SCORES[my_move]
      score = outcome + shape_score
      print(f'{opponent_move} vs {my_move} -> {outcome=} + {shape_score=} = {score=}')
      total_score += score
  print('Total score:', total_score)


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
