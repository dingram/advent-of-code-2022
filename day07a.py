#!/usr/bin/env python3
from collections.abc import Sequence
import os
import sys
from typing import TextIO


def main(argv0: str, args: Sequence[str]) -> None:
  if len(args) != 1:
    raise Exception(f'Usage: {argv0} <filename>')

  with open(args[0], 'rt') as input_file:
    directory_tree = parse_input(input_file)
    dump_tree(directory_tree)

    total = 0
    for path, size in directory_tree.items():
      if not path.endswith('/'):
        # Ignore files
        continue
      if path == '/':
        # Ignore the root directory
        continue
      if size > 100000:
        # Ignore directories larger than a certain size
        continue
      total += size
    print(total)


def dump_tree(tree: dict[str, int]) -> None:
  max_len = max(len(p) for p in tree)
  for path, size in sorted(tree.items()):
    print(f'{path:{max_len}}  {size}')
  print()


def parse_input(f: TextIO) -> dict[str, int]:
  # Current working directory, as a string.
  cwd: str = '/'

  # Directory tree, mapping path to size. If the path ends with "/", it's a
  # directory, and the size is the total size of the directory's contents.
  tree: dict[str, int] = {'/': 0}

  for line in f:
    line = line.strip()
    if line.startswith('$ cd'):
      # Change directory
      target = line[5:]
      if target == '..':
        # Remove the last directory element in the current working directory.
        cwd = os.path.dirname(cwd)
      elif target == '/':
        # Reset to the root directory.
        cwd = '/'
      else:
        # Add to the current working directory.
        cwd = os.path.join(cwd, target)
    elif line.startswith('$ ls'):
      # List files; ignore, because we assume everything else is a listing
      pass
    elif line.startswith('dir'):
      # Found a directory
      dirname = line[4:]
      # Add its entry to the directory tree if not already present
      tree.setdefault(os.path.join(cwd, dirname) + '/', 0)
    else:
      # Found a file
      size, filename = line.split(' ', 1)
      size = int(size)
      # Add its entry to the directory tree
      full_filename = os.path.join(cwd, filename)
      tree[full_filename] = size
      # Update the parent directory sizes
      parent_dir = os.path.dirname(full_filename)
      while parent_dir != '/':
        tree[parent_dir + '/'] += size
        parent_dir = os.path.dirname(parent_dir)
      tree['/'] += size

  return tree


if __name__ == '__main__':
  main(sys.argv[0], sys.argv[1:])
