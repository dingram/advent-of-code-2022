#!/usr/bin/env python3
from collections.abc import Iterable, Sequence
import itertools
import sys
from typing import TextIO


def grouper(iterable: Iterable[str]):
  args = [iter(iterable)] * 3
  return zip(*args)


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    priority_sum = 0
    for line1, line2, line3 in grouper(input_file):
      line1 = line1.strip()
      line2 = line2.strip()
      line3 = line3.strip()

      shared_item = next(iter(
          set(line1).intersection(line2).intersection(line3)))
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
