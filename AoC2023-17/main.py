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
      self.map_data[layer] = [ [int(tile) for tile in line.strip()] for line in file]

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

class Path:
  
  def __init__(self,pos,dir):
    self.pos = pos
    self.length = 0
    self.dir = dir
    self.dir_steps = 0
    self.history = [pos]

  def __repr__(self):
    s = 'Length: {}, pos: {}, dir: {} [{}]\n'.format( \
      self.length,self.pos,self.dir,self.dir_steps)
    s += 'History:\n'
    for state in self.history:
      s+= str(state) + '\n'
    return s

  def state(self):
    return (self.pos, self.dir, self.dir_steps)
    
  def __eq__(self,other):
    return (self.pos == other.pos) and \
    (self.dir == other.dir) and (self.dir_steps == other.dir_steps)
    
  def __gt__(self,other):
    return self.length > other.length

  def copy(self):
    c = Path(self.pos,self.dir)
    c.length = self.length
    c.dir_steps = self.dir_steps
    c.history = self.history.copy()
    return c
    
  def step(self,d=None):
    if not d:
      d = self.dir
    self.pos = (self.pos[0] + d[0], self.pos[1] + d[1])
    self.history.append(self.pos)

  def draw_path(self,map):
    for y in range(map.height()):
      s = ''
      for x in range(map.width()):
        if (x,y) in self.history:
          s += '@' if (x,y) == self.pos else '#'
        else:
          s += str(map.get_tile((x,y)))
      print(s)
    
def part1(map):
  paths = SortedList()
  paths.add( Path( (0,0), (1,0) ) )
  previous = {}
  while paths:
    p = paths.pop(0)
    if p.pos == (map.width()-1,map.height()-1):
      #p.draw_path(map)
      print('Heat loss:', p.length)
      break
    for dir in [(0,1), (0,-1), (1,0), (-1,0)]:
      q = p.copy()
      q.dir = dir
      # No reversing
      if q.dir == (-p.dir[0], -p.dir[1]):
        continue
      q.dir_steps = p.dir_steps + 1 if q.dir == p.dir else 1
      # Max three steps in one direction
      if q.dir_steps > 3:
        continue
      q.step()
      # No going out of bounds
      if q.pos[0] < 0 or q.pos[0] >= map.width() or \
      q.pos[1] < 0 or q.pos[1] >= map.height():
        continue
      q.length += map.get_tile(q.pos)
      # Check if we've been here before
      before = previous.get( q.state(), None )
      if before and before <= q.length:
        continue
      previous[q.state()] = q.length
      # Fork off
      paths.add( q )

def part2(map):
  paths = SortedList()
  paths.add( Path( (0,0), (1,0) ) )
  previous = {}
  while paths:
    p = paths.pop(0)
    if p.pos == (map.width()-1,map.height()-1) and p.dir_steps >= 4:
      #p.draw_path(map)
      print('Heat loss:', p.length)
      break
    for dir in [(0,1), (0,-1), (1,0), (-1,0)]:
      q = p.copy()
      q.dir = dir
      # No reversing
      if q.dir == (-p.dir[0], -p.dir[1]):
        continue
      # Min four steps in one direction
      if p.dir_steps < 4 and q.dir != p.dir:
        continue      
      q.dir_steps = p.dir_steps + 1 if q.dir == p.dir else 1
      # Max ten steps in one direction
      if q.dir_steps > 10:
        continue
      q.step()
      # No going out of bounds
      if q.pos[0] < 0 or q.pos[0] >= map.width() or \
      q.pos[1] < 0 or q.pos[1] >= map.height():
        continue
      q.length += map.get_tile(q.pos)
      # Check if we've been here before
      before = previous.get( q.state(), None )
      if before and before <= q.length:
        continue
      previous[q.state()] = q.length
      # Fork off
      paths.add( q )
    
map = Map('input.dat')
part2(map)