#!/usr/bin/env python3
from collections.abc import Sequence
import sys
from typing import TextIO


ROPE_LENGTH = 2
DIRECTION_VECTORS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

# Part 1
MIN_W = 0
MAX_W = 6
MIN_H = 0
MAX_H = 4

# Part 2
#MIN_W = -11
#MAX_W = 14
#MIN_H = -5
#MAX_H = 14


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    instructions = parse_input(input_file)

    rope = [(0, 0)] * ROPE_LENGTH
    tail_visited = {rope[-1]}
    print('== Initial state ==\n')
    print_state(rope)

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
  print(f'== {instruction[0]} {instruction[1]} ==\n')
  if instruction[0].startswith('#'):
    return rope
  direction = DIRECTION_VECTORS[instruction[0]]
  for _ in range(instruction[1]):
    rope = step(direction, rope)
    print_state(rope)
    tail_visited.add(rope[-1])
  #print_state(rope)
  return rope


def sign(v: int) -> int:
  return 0 if v == 0 else v // abs(v)


def step(
    direction: tuple[int, int],
    rope: list[tuple[int, int]]) -> list[tuple[int, int]]:

  # Move head
  prev_x, prev_y = rope[0]
  new_x = prev_x + direction[0]
  new_y = prev_y + direction[1]
  new_rope = [(new_x, new_y)]

  for knot, orig_prev_knot in zip(rope[1:], rope):
    new_rope.append(step_knot(new_rope[-1], orig_prev_knot, knot))

  return new_rope


def step_knot(
    new_prev_knot: tuple[int, int],
    orig_prev_knot: tuple[int, int],
    current_knot: tuple[int, int]) -> tuple[int, int]:

  knot_x, knot_y = current_knot

  # If knot is less than two spaces from the previous one's new position, it
  # stays where it is.
  diff_x = knot_x - new_prev_knot[0]
  diff_y = knot_y - new_prev_knot[1]
  if abs(diff_x) <= 1 and abs(diff_y) <= 1:
    return current_knot

  if knot_x == new_prev_knot[0]:
    # Same row; bump knot_y
    knot_y = orig_prev_knot[1]
  elif knot_y == new_prev_knot[1]:
    # Same column; bump knot_x
    knot_x = orig_prev_knot[0]
  else:
    # Move diagonally.
    print('Move diagonally')
    return current_knot

  return knot_x, knot_y


def print_state(rope: list[tuple[int, int]]) -> None:
  #print(rope)
  for y in reversed(range(MIN_H, MAX_H + 1)):
    for x in range(MIN_W, MAX_W + 1):
      here = (x, -y)
      if here in rope:
        here_idx = rope.index(here) or 'H'
        if ROPE_LENGTH == 2 and here_idx == 1:
          here_idx = 'T'
        print(here_idx, end='')
      elif here == (0, 0):
        print('s', end='')
      else:
        print('.', end='')
    print()
  print()


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
