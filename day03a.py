#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    priority_sum = 0
    for line in input_file:
      line = line.strip()
      part1, part2 = line[:len(line)//2], line[len(line)//2:]
      shared_item = next(iter(set(part1).intersection(part2)))
      priority_sum += get_priority(shared_item)
    print(priority_sum)


def get_priority(c: str) -> int:
  if c.islower():
    return 1 + ord(c) - ord('a')
  elif c.isupper():
    return 27 + ord(c) - ord('A')
  else:
    raise ValueError


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
