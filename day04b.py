#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    pairs = parse_pairs(input_file)
    #print(pairs)
    complete_inclusions = sum(1 if includes(*p) else 0 for p in pairs)
    print(complete_inclusions)
    overlaps = sum(1 if any_overlap(*p) else 0 for p in pairs)
    print(overlaps)


def parse_pairs(f: TextIO) -> Sequence[tuple[tuple[int, int]]]:
  result = []
  for line in f:
    line = line.strip()
    result.append(
        tuple(tuple(int(v) for v in p.split('-')) for p in line.split(',')))
  return result


def includes(a, b) -> bool:
  if a[0] <= b[0]  and a[1] >= b[1]:
    return True
  if b[0] <= a[0]  and b[1] >= a[1]:
    return True
  return False


def any_overlap(a, b) -> bool:
  return not (a[1] < b[0] or b[1] < a[0])

if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
