#!/usr/bin/env python3
from collections.abc import Sequence
import itertools
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    grid = parse_input(input_file)
    print('Visible trees:', number_of_visible_trees(grid))
    print('Max scenic score:', max_scenic_score(grid))


def parse_input(input_file: TextIO) -> list[list[int]]:
  return [[int(c) for c in line.strip()] for line in input_file]


def number_of_visible_trees(grid: list[list[int]]) -> int:
  # Construct a grid of booleans for whether a tree is visible or not, and
  # start with them all invisible.
  visibility = [[False] * len(grid[0]) for _ in range(len(grid))]

  # First, traverse the grid top to bottom, left to right
  high_water_col = [-1] * len(grid[0])
  # The next line could also be written as...
  #    for row_idx in range(len(grid)):
  #      row = grid[row_idx]
  for row_idx, row in enumerate(grid):
    high_water_row = -1
    for col_idx, v in enumerate(row):
      if v > high_water_row or v > high_water_col[col_idx]:
        # Visible from the left or above
        visibility[row_idx][col_idx] = True
      # Update high-water marks
      high_water_row = max(high_water_row, v)
      high_water_col[col_idx] = max(high_water_col[col_idx], v)

  # Then, traverse the grid bottom to top, right to left (and reset high-water
  # marks). It's important that we reverse/enumerate in this order, so that the
  # indexes match what we've already done. Otherwise this code would update the
  # mirror-image visibility instead. We also have to turn the enumeration into
  # a list so it can be reversed.
  high_water_col = [-1] * len(grid[0])
  for row_idx, row in reversed(list(enumerate(grid))):
    high_water_row = -1
    for col_idx, v in reversed(list(enumerate(row))):
      if v > high_water_row or v > high_water_col[col_idx]:
        # Visible from the right or below
        visibility[row_idx][col_idx] = True
      # Update high-water marks
      high_water_row = max(high_water_row, v)
      high_water_col[col_idx] = max(high_water_col[col_idx], v)

  return sum(int(v) for v in itertools.chain.from_iterable(visibility))


def count_visible(this: int, trees: list[int]) -> int:
  visible = 0
  for tree in trees:
    visible += 1
    if tree >= this:
      break
  return visible


def scenic_score(grid: list[list[int]], row_idx: int, col_idx: int) -> int:
  score_l, score_r, score_u, score_d = 0, 0, 0, 0
  row = list(grid[row_idx])
  col = [grid[r][col_idx] for r in range(len(grid))]
  this = grid[row_idx][col_idx]

  # Trees to the left and right
  score_l = count_visible(this, list(reversed(row[:col_idx])))
  score_r = count_visible(this, row[col_idx + 1:])
  # Trees above and below
  score_u = count_visible(this, list(reversed(col[:row_idx])))
  score_d = count_visible(this, col[row_idx + 1:])

  return score_l * score_r * score_u * score_d


def max_scenic_score(grid: list[list[int]]) -> int:
  scenic_scores = [
      [scenic_score(grid, row_idx, col_idx) for col_idx in range(len(grid[row_idx]))]
      for row_idx in range(len(grid))]
  return max(itertools.chain.from_iterable(scenic_scores))


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
