#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    # Turn input into individual elves.
    elves = parse_elves(input_file)

    print('Biggest elf:', max(elves))


def parse_elves(input_file: TextIO) -> Sequence[int]:
  elves = []
  current_elf = 0
  for line in input_file:
    line = line.strip()
    if line:
      current_elf += int(line)
    else:
      elves.append(current_elf)
      current_elf = 0

  # If we have a remaining elf, add that to the list
  if current_elf:
    elves.append(current_elf)
  return elves


def parse_elves_alternative(input_file: TextIO) -> Sequence[int]:
  elves = [0]
  for line in input_file:
    line = line.strip()
    if line:
      elves[-1] += int(line)
    else:
      elves.append(0)
  if not elves[-1]:
    # Drop the last elf if it has zero calories, though this doesn't really
    # matter in any way.
    elves.pop()
  return elves


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
