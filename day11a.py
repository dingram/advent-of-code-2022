#!/usr/bin/env python3
from collections.abc import Sequence
import dataclasses
import re
import sys
from typing import TextIO


@dataclasses.dataclass
class Monkey:
  number: int
  items: list[int]
  operator: str
  operand: int
  test: int
  true_target: int
  false_target: int


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    print(parse_input(input_file))


def parse_input(input_file: TextIO) -> list[Monkey]:
  monkeys = []
  acc = []
  for line in input_file:
    line = line.strip()
    if line:
      acc.append(line)
    else:
      monkeys.append(parse_monkey(acc))
      acc = []
  if acc:
    monkeys.append(parse_monkey(acc))
  return monkeys


def parse_monkey(lines: list[str]) -> Monkey:
  number = int(re.sub(r'[^0-9]+', '', lines[0]))
  for line in lines[1:]:
    key, value = line.split(': ')
    if key == 'Starting items':
      items = [int(v) for v in value.split(', ')]
    elif key == 'Operation':
      operator, op = value.split(' ')[-2:]
      if op == 'old':
        operator = '**'
        operand = 2
      else:
        operand = int(op)
    elif key == 'Test':
      test = int(value.split(' ')[-1])
    elif key == 'If true':
      true_target = int(value.split(' ')[-1])
    elif key == 'If false':
      false_target = int(value.split(' ')[-1])
    else:
      raise ValueError(line)
  return Monkey(
      number=number,
      items=items,
      operator=operator,
      operand=operand,
      test=test,
      true_target=true_target,
      false_target=false_target,
  )


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
