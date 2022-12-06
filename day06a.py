#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    data = input_file.read().strip()
    for c in range(len(data) - 3):
      if len(set(data[c:c + 4])) == 4:
        print(c + 4)
        break


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
