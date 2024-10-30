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
    self.set_origin( (0,0) )

  def __repr__(self):
    s = ''
    for layer in self.map_data:
      s += ''.join([''.join([''.join([str(tile) for tile in row])+'\n' \
                             for row in self.map_data[layer]])+'\n'])
    return s

  def load_data( self, file_name, layer='default' ):
    with open(file_name,'r') as file:
      self.map_data[layer] = [ [tile for tile in line.strip()] for line in file]

  def set_origin(self, o):
    self.origin = o
    
  def width(self, layer='default'):
    return len(self.map_data[layer][0]) if len(self.map_data[layer]) > 0 else 0

  def height(self, layer='default'):
    return len(self.map_data[layer])

  def fill_map(self, x, y, tile = '.', layer='default'):
    self.map_data[layer] = [ [ tile for col in range(x) ] for row in range(y) ]

  def is_valid_pos(self, pos, wrap = 0, layer='default'):
    x = pos[0] + self.origin[0]
    y = pos[1] + self.origin[1]
    w = self.width(layer)
    h = self.height(layer)
    return (y >= -wrap*h and y < (wrap+1) * h and \
            x >= -wrap*w and x < (wrap+1) * w)

  def get_tile(self, pos, wrap = 0, layer='default'):
    if self.is_valid_pos(pos,wrap):
      return self.map_data[layer] \
      [(pos[1]+self.origin[1])%self.height()] \
      [(pos[0]+self.origin[0])%self.width()]
    else:
      raise IndexError

  def set_tile(self,pos,tile, layer='default'):
    if not self.is_valid_pos(pos,layer):
      raise IndexError
    self.map_data[layer][pos[1]+self.origin[1]][pos[0]+self.origin[0]] = tile

  def find_tile(self, tile, layer='default'):
    for y, line in enumerate(self.map_data[layer]):
      with suppress(ValueError):
        return (line.index(tile)-self.origin[0],y-self.origin[1])
    return (None,None)

  def count(self,tile, layer='default'):
    n = 0
    for line in self.map_data[layer]:
      n += line.count(tile)
    return n

  def count_sectorwise(self,reached_tiles,steps):
    counts = {}
    for p, s in reached_tiles.items():
      if s > steps:
        continue
      s_x = (p[0]+self.origin[0]) // self.width()
      s_y = (p[1]+self.origin[1]) // self.height()
      sec = (s_x,s_y)
      evenodd = counts.setdefault(sec,[0,0])
      if (s-steps)%2 == 0:
        evenodd[0] += 1
      else:
        evenodd[1] += 1
    return counts

  def count_all(self,reached_tiles,steps):
    counts = 0
    for v in reached_tiles.values():
      counts += 1 if v <= steps and (v - steps) % 2 == 0 else 0
    return counts

  def walk(self, needed_steps, start_pos = None, wrap = 0):
    if not start_pos:
      start_pos = self.find_tile('S')
    steps = 0
    reached_tiles = {}
    reached_tiles[start_pos] = steps
    frontiers = SortedList([(steps,start_pos)])
    while frontiers:
      steps, pos = frontiers.pop(0)
      if steps == needed_steps:
        continue
      for dir in [(1,0), (-1,0), (0,1), (0,-1)]:
        new_pos = (pos[0]+dir[0],pos[1]+dir[1])
        try:
          if self.get_tile(new_pos, wrap) in ['.', 'S']:
            if new_pos not in reached_tiles:
              frontiers.add((steps+1,new_pos))
              reached_tiles[new_pos] = steps+1
        except IndexError:
          continue
    return reached_tiles

def part2(map):
  w = map.width()
  h = map.height()
  map.set_origin( (w//2+1,h//2+1) )
  needed_steps = 26501365
  macro_steps = max(0,(needed_steps-w//2-2*w) // w)
  micro_steps = needed_steps - macro_steps*w
  sec77 = map.walk(micro_steps, start_pos = map.find_tile('S'), wrap = 3)
  counts = map.count_sectorwise(sec77,needed_steps)
  m = (macro_steps+1)//2
  n_same_parity = 1 + 4*m*(m+1)
  m = macro_steps//2
  n_diff_parity = 4*(m+1)*(m+1)
  mod = (needed_steps - micro_steps) % 2
  c_infill = n_same_parity * counts[(0,0)][0] + n_diff_parity * counts[(0,0)][1]
  c_xs = (macro_steps + 2) * (counts[(2,1)][mod] + counts[(2,-1)][mod] + \
     counts[(-2,1)][mod] + counts[(-2,-1)][mod])
  c_bs = (macro_steps + 1) * (counts[(1,1)][mod] + counts[(1,-1)][mod] + \
     counts[(-1,1)][mod] + counts[(-1,-1)][mod])
  c_ends = (counts[(2,0)][mod] + counts[(-2,0)][mod] + \
     counts[(0,2)][mod]+counts[(0,-2)][mod])
  c_overshoot = counts.get((3,0),[0,0])[mod] + counts.get((-3,0),[0,0])[mod] + \
     counts.get((0,3),[0,0])[mod] + counts.get((0,-3),[0,0])[mod]
  c_spill = (macro_steps+3) * \
  (counts.get((2,2),[0,0])[mod] + counts.get((2,-2),[0,0])[mod] + \
   counts.get((-2,2),[0,0])[mod] + counts.get((-2,-2),[0,0])[mod])
  total = c_infill + c_xs + c_bs + c_ends + c_overshoot + c_spill

  #test = map.walk(needed_steps, start_pos = map.find_tile('S'), wrap = 100)
  #test_count = map.count_sectorwise(test,needed_steps)
  #for sec, c in sorted(test_count.items()):
  #  print(sec, ':', c,'    ', counts.get(sec,0))
  #print('check:', map.count_all( test, needed_steps ) )

  print('Macro steps:', macro_steps, 'Micro steps:', micro_steps)
  return total

map = Map('input.dat')
print('Part 2:', part2(map))