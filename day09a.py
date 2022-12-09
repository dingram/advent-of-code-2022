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

    head_pos = (0, 0)
    tail_pos = (0, 0)
    tail_visited = {tail_pos}
    #print('== Initial state ==\n')
    #print_state(head_pos, tail_pos)

    for instruction in instructions:
      head_pos, tail_pos = move(instruction, head_pos, tail_pos, tail_visited)

    print('Tail visited positions:', len(tail_visited))


def parse_input(input_file: TextIO) -> Sequence[tuple[str, int]]:
  instructions = []
  for line in input_file:
    direction, distance = line.strip().split(' ')
    instructions.append((direction, int(distance)))
  return instructions


def move(
    instruction: tuple[str, int],
    head_pos: tuple[int, int],
    tail_pos: tuple[int, int],
    tail_visited: set[tuple[int, int]]
  ) -> tuple[tuple[int, int], tuple[int, int]]:
  #print(f'== {instruction[0]} {instruction[1]} ==\n')
  direction = DIRECTION_VECTORS[instruction[0]]
  for _ in range(instruction[1]):
    head_pos, tail_pos = step(direction, head_pos, tail_pos)
    tail_visited.add(tail_pos)
  return head_pos, tail_pos


def step(
    direction: tuple[int, int],
    head_pos: tuple[int, int],
    tail_pos: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
  head_x, head_y = head_pos
  tail_x, tail_y = tail_pos

  # Move head
  new_head_x = head_x + direction[0]
  new_head_y = head_y + direction[1]

  # If tail is more than one space from the head, it has to move.
  if abs(tail_x - new_head_x) > 1 or abs(tail_y - new_head_y) > 1:
    if tail_x == new_head_x:
      # Same row; bump tail_y
      tail_y += direction[1]
    elif tail_y == new_head_y:
      # Same column; bump tail_x
      tail_x += direction[0]
    else:
      # Move diagonally, to where head used to be
      tail_x = head_x
      tail_y = head_y

  new_head_pos = (new_head_x, new_head_y)
  new_tail_pos = (tail_x, tail_y)
  #print_state(new_head_pos, new_tail_pos)
  return new_head_pos, new_tail_pos


def print_state(head_pos: tuple[int, int], tail_pos: tuple[int, int]) -> None:
  for y in reversed(range(HEIGHT)):
    for x in range(WIDTH):
      here = (x, -y)
      if head_pos == here:
        print('H', end='')
      elif tail_pos == here:
        print('T', end='')
      elif (0, 0) == here:
        print('s', end='')
      else:
        print('.', end='')
    print()
  print()


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
