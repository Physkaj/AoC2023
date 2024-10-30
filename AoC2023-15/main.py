from copy import deepcopy
import re
from collections import deque
from contextlib import suppress


def arrange_data(data):
  return [re.split(r'(-|=)',w) for w in data[0].split(',')]

def load_data( file_name ):
  with open(file_name,'r') as file:
    data = [ line.strip() for line in file]
  return arrange_data(data)

def calc_hash(str):
  hash = 0
  for c in str:
    hash += ord(c)
    hash *= 17
    hash %= 256
  return hash

def part1(data):
  hash_sum = 0
  for cmd in data:
    hash_sum += calc_hash(''.join(cmd))
  print(hash_sum)

def calc_focusing_power( boxes, focal_lengths ):
  fp = 0
  for b, box in enumerate(boxes):
    for l, lens in enumerate(box):
      fp += (b+1)*(l+1)*focal_lengths[lens]
  return fp

def part2(data):
  print( calc_focusing_power( *process_cmds(data) ) )

def process_cmds(data):
  boxes = [deque() for n in range(256)]
  lens_focusing_power = {}
  for cmd in data:
    box_index = calc_hash(cmd[0])
    match cmd[1]:
      case '-':
        # Remove lens if present
        with suppress(ValueError):
          boxes[box_index].remove(cmd[0])
      case '=':
        if not boxes[box_index].count(cmd[0]):
          boxes[box_index].append( cmd[0] )
        lens_focusing_power[cmd[0]] = int(cmd[2])
  return (boxes, lens_focusing_power)

data = load_data('input.dat')

part2(data)


