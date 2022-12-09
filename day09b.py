#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


DIRECTION_VECTORS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}
WIDTH = 6
HEIGHT = 5


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    instructions = parse_input(input_file)

    rope = [(0, 0)] * 2
    tail_visited = {rope[-1]}
    #print('== Initial state ==\n')
    #print_state(rope)

    for instruction in instructions:
      rope = move(instruction, rope, tail_visited)

    print('Tail visited positions:', len(tail_visited))


def parse_input(input_file: TextIO) -> Sequence[tuple[str, int]]:
  instructions = []
  for line in input_file:
    direction, distance = line.strip().split(' ')
    instructions.append((direction, int(distance)))
  return instructions


def move(
    instruction: tuple[str, int],
    rope: list[tuple[int, int]],
    tail_visited: set[tuple[int, int]]
  ) -> list[tuple[int, int]]:
  #print(f'== {instruction[0]} {instruction[1]} ==\n')
  direction = DIRECTION_VECTORS[instruction[0]]
  for _ in range(instruction[1]):
    rope = step(direction, rope)
    tail_visited.add(rope[-1])
  return rope


def step(
    direction: tuple[int, int],
    rope: list[tuple[int, int]]) -> list[tuple[int, int]]:

  # Move head
  prev_x, prev_y = rope[0]
  new_x = prev_x + direction[0]
  new_y = prev_y + direction[1]
  new_rope = [(new_x, new_y)]

  for knot in rope[1:]:
    knot_x, knot_y = knot
    # If knot is more than one space from the previous one, it has to move.
    if abs(knot_x - new_x) > 1 or abs(knot_y - new_y) > 1:
      if knot_x == new_x:
        # Same row; bump knot_y
        new_y = knot_y + direction[1]
      elif knot_y == new_y:
        # Same column; bump knot_x
        new_x = knot_x + direction[0]
      else:
        # Move diagonally, to where head used to be
        new_x = prev_x
        new_y = prev_y
    else:
      new_x, new_y = knot_x, knot_y
    new_rope.append((new_x, new_y))
    prev_x, prev_y = knot_x, knot_y

  #print_state(new_rope)
  return new_rope


def print_state(rope: list[tuple[int, int]]) -> None:
  for y in reversed(range(HEIGHT)):
    for x in range(WIDTH):
      here = (x, -y)
      if here == rope[0]:
        print('H', end='')
      elif here == rope[1]:
        print('T', end='')
      elif here == (0, 0):
        print('s', end='')
      else:
        print('.', end='')
    print()
  print()


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
