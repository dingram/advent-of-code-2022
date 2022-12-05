#!/usr/bin/env python3
from collections.abc import Sequence
import re
import sys
from typing import TextIO

import day05_parser


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    stacks, instructions = day05_parser.parse_input(input_file)
    for count, from_stack, to_stack in instructions:
      crate_group = []
      for _ in range(count):
        crate_group.append(stacks[from_stack - 1].pop())
      stacks[to_stack - 1].extend(reversed(crate_group))

  print(''.join(c[-1] for c in stacks if c))


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
