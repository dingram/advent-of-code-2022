#!/usr/bin/env python3
from collections.abc import Sequence
import dataclasses
import math
import re
import sys
from typing import TextIO


_DETAILED_TURN = False


@dataclasses.dataclass
class Monkey:
  number: int
  items: list[int]
  operator: str
  operand: int
  test: int
  true_target: int
  false_target: int
  inspections: int = 0


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    monkeys = parse_input(input_file)
    #print(monkeys)

    base = math.lcm(*(m.test for m in monkeys))

    for round_idx in range(1, 10001):
      print(f'Starting round {round_idx}...')
      for idx in range(len(monkeys)):
        monkeys = take_turn(monkeys, idx, base)
      #print(f'\nAfter round {round_idx}, the monkeys are holding items with these worry levels:')
      #for monkey in monkeys:
      #  print(f'Monkey {monkey.number}: {", ".join(str(i) for i in monkey.items)}')

    print()
    for monkey in monkeys:
      print(f'Monkey {monkey.number} inspected items {monkey.inspections} times')

    top_2 = list(sorted(monkeys, key=lambda m: m.inspections))[-2:]
    print('Final result: ', top_2[0].inspections * top_2[1].inspections)


def take_turn(monkeys: list[Monkey], monkey_id: int, base: int) -> list[Monkey]:
  current_monkey = monkeys[monkey_id]
  if _DETAILED_TURN:
    print(f'\nMonkey {monkey_id}:')
  if current_monkey.operator == '+':
    action = f'increases by {current_monkey.operand}'
    modify = lambda x: x + current_monkey.operand
  elif current_monkey.operator == '*':
    action = f'is multiplied by {current_monkey.operand}'
    modify = lambda x: x * current_monkey.operand
  elif current_monkey.operator == '**':
    action = f'is multiplied by itself'
    modify = lambda x: x * x

  for item in current_monkey.items:
    current_monkey.inspections += 1
    if _DETAILED_TURN:
      print(f'  Monkey inspects an item with a worry level of {item}.')
    new_worry = modify(item)
    if _DETAILED_TURN:
      print(f'    Worry level {action} to {new_worry}.')

    new_worry = new_worry % base

    if new_worry % current_monkey.test:
      if _DETAILED_TURN:
        print(f'    Current worry level is not divisible by {current_monkey.test}.')
      target = current_monkey.false_target
    else:
      if _DETAILED_TURN:
        print(f'    Current worry level is divisible by {current_monkey.test}.')
      target = current_monkey.true_target
    monkeys[target].items.append(new_worry)
    if _DETAILED_TURN:
      print(f'    Item with worry level {new_worry} is thrown to monkey {target}.')
  current_monkey.items = []

  return monkeys


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
