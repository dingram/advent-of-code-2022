#!/usr/bin/env python3
from collections.abc import Sequence
import re
import sys
from typing import TextIO

NUM_CRATES = 9


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    crates, instructions = parse_input(input_file)
    for count, from_crate, to_crate in instructions:
      being_moved = []
      for _ in range(count):
        being_moved.append(crates[from_crate - 1].pop())
      crates[to_crate - 1].extend(reversed(being_moved))
    print(crates)

  print(''.join(c[-1] for c in crates if c))


def parse_input(f: TextIO) -> ...:
  crate_lines = []
  instructions = []
  for line in f:
    if '[' in line:
      crate_lines.append(line)
    if 'move' in line:
      instructions.append(tuple(
          int(v) for v in re.search(r'move (\d+) from (\d+) to (\d+)',
              line).group(1, 2, 3)))

  crates = [[] for _ in range(NUM_CRATES)]
  for line in reversed(crate_lines):
    for n in range(NUM_CRATES):
      if 1 + 4 * n < len(line):
        if (c := line[1 + 4*n]) != ' ':
          crates[n].append(c)

  return crates, instructions


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
