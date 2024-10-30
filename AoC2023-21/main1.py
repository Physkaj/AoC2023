import re
from collections import deque
from contextlib import suppress
from copy import deepcopy
from sortedcontainers import SortedList


class Map:

  def __init__(self, file_name = ''):
    self.map_data = {}
    if file_name:
      self.load_data(file_name)


  def __repr__(self):
    s = ''
    for layer in self.map_data:
      s += ''.join([''.join([''.join([str(tile) for tile in row])+'\n' \
                             for row in self.map_data[layer]])+'\n'])
    return s

  def load_data( self, file_name, layer='default' ):
    with open(file_name,'r') as file:
      self.map_data[layer] = [ [tile for tile in line.strip()] for line in file]

  def width(self, layer='default'):
    return len(self.map_data[layer][0]) if len(self.map_data[layer]) > 0 else 0

  def height(self, layer='default'):
    return len(self.map_data[layer])

  def fill_map(self, x, y, tile = '.', layer='default'):
    self.map_data[layer] = [ [ tile for col in range(x) ] for row in range(y) ]

  def is_valid_pos(self,pos, layer='default'):
    return \
    (pos[1] >= 0 and pos[1] < len(self.map_data[layer]) and \
    pos[0] >= 0 and pos[0] < len(self.map_data[layer][pos[1]]))

  def get_tile(self, pos, layer='default'):
    if not self.is_valid_pos(pos,layer):
      raise IndexError
    return self.map_data[layer][pos[1]][pos[0]]

  def set_tile(self,pos,tile, layer='default'):
    if not self.is_valid_pos(pos,layer):
      raise IndexError
    self.map_data[layer][pos[1]][pos[0]] = tile

  def find_tile(self, tile, layer='default'):
    for y, line in enumerate(self.map_data[layer]):
      with suppress(ValueError):
        return (line.index(tile),y)
    return (None,None)

  def count(self,tile, layer='default'):
    n = 0
    for line in self.map_data[layer]:
      n += line.count(tile)
    return n

def part1():
  map = Map('input.dat')
  start_pos = map.find_tile('S')
  steps = 0
  reached_tiles = {}
  reached_tiles[start_pos] = steps
  frontiers = SortedList([(steps,start_pos)])
  while frontiers:
    steps, pos = frontiers.pop(0)
    if steps == 64:
      continue
    for dir in [(1,0), (-1,0), (0,1), (0,-1)]:
      new_pos = (pos[0]+dir[0],pos[1]+dir[1])
      try:
        if map.get_tile(new_pos) in ['.', 'S']:
          if new_pos not in reached_tiles:
            frontiers.add((steps+1,new_pos))
            reached_tiles[new_pos] = steps+1
      except IndexError:
        continue
  return len( [s for s in reached_tiles.values() if s % 2 == 0])

print('Part 1:',part1())