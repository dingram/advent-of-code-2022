#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    instructions = parse_input(input_file)

    # Represents the value of X _during_ each cycle... e.g. during cycle 0, X=1
    reg_x = [1]

    for cycle_length, x_inc in instructions:
      for _ in range(cycle_length - 1):
        reg_x.append(reg_x[-1])
      reg_x.append(reg_x[-1] + x_inc)

    # We don't care about its value after the last instruction, only during.
    reg_x.pop()

    # Now render the display.
    for idx, x in enumerate(reg_x):
      if abs((idx % 40) - x) <= 1:
        print('#', end='')
      else:
        print('.', end='')
      if (idx + 1) % 40 == 0:
        print()


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
