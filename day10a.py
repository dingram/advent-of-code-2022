#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    instructions = parse_input(input_file)

    reg_x = 1
    cycle_count = 0
    strength: dict[int, int] = {}

    for cycle_length, x_inc in instructions:
      cycle_count += cycle_length
      if cycle_count % 40 == 20:
        print(f'During cycle {cycle_count}, X = {reg_x}')
        strength[cycle_count] = reg_x
      elif cycle_count % 40 == 21 and (cycle_count - 1) not in strength:
        print(f'During cycle {cycle_count - 1}, X = {reg_x}')
        strength[cycle_count - 1] = reg_x
      reg_x += x_inc

    print(f'Final X = {reg_x}')
    total_strength = sum(a * b for a, b in strength.items())
    print(f'Total strength = {total_strength}')


def parse_input(input_file: TextIO) -> list[tuple[int, int]]:
  result = []
  # Output: (cycle length, X increment)
  for line in input_file:
    if line.startswith('noop'):
      result.append((1, 0))
    elif line.startswith('addx'):
      result.append((2, int(line.strip().split(' ')[1])))
    else:
      raise ValueError(line)
  return result


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
