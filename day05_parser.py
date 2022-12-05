import re


def parse_input(input_file):
  crate_lines = []
  instructions = []
  for line in input_file:
    # Contains a crate
    if '[' in line:
      crate_lines.append(line)
    # Contains a 'move' instruction
    if 'move' in line:
      # Parse the instruction.
      re_result = re.search(r'move (\d+) from (\d+) to (\d+)', line)
      # Convert string match groups to ints, which are easier to work with.
      instruction = tuple(int(v) for v in re_result.group(1, 2, 3))
      instructions.append(instruction)

  # There's one '[' per crate in each line, assuming that no stack is empty.
  stack_count = crate_lines[-1].count('[')

  # Note: don't use [[]] * stack_count, or each element will be the _same_ list
  # instance, which would mean all operations happen on a single list.
  stacks = [[] for _ in range(stack_count)]

  # Iterate over the crate lines in reverse order, so the first element in each
  # resulting list is the bottom of the stack.
  for line in reversed(crate_lines):
    # For each stack...
    for n in range(stack_count):
      # The (1+4n)th character is the crate ID.
      crate_id_idx = 1 + 4 * n
      if crate_id_idx >= len(line):
        # Be defensive, just in case there are no trailing spaces.
        continue
      crate_id = line[crate_id_idx]
      if crate_id != ' ':
        stacks[n].append(crate_id)

  return stacks, instructions
