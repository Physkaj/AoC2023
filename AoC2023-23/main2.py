import re
from collections import deque
from contextlib import suppress
from copy import deepcopy
from sortedcontainers import SortedList

directions = {'E':(0,1), 'W':(0,-1), 'S':(1,0), 'N':(-1,0)}

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

  def is_valid_pos(self, pos, layer='default'):
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

  def __init__(self,pos):
    self.pos = pos
    self.length = 0
    self.history = {pos: self.length}

  def __repr__(self):
    s = 'Length: {}, pos: {}\n'.format( \
      self.length,self.pos)
    s += 'History:\n'
    for state in self.history:
      s+= str(state) + '\n'
    return s

  def __eq__(self,other):
    return self.pos == other.pos

  def __gt__(self,other):
    return self.length > other.length

  def copy(self):
    c = Path(self.pos)
    c.length = self.length
    c.history = self.history.copy()
    return c

  def step(self,d):
    self.pos = (self.pos[0] + d[0], self.pos[1] + d[1])
    self.length += 1

  def record_step(self,possibilities):
    self.history[self.pos] = possibilities

  def draw_path(self,map):
    for y in range(map.height()):
      s = ''
      for x in range(map.width()):
        if (x,y) in self.history:
          s += '@' if (x,y) == self.pos else 'O'
        else:
          s += str(map.get_tile((x,y)))
      print(s)

def find_start_position(map):
  for x in range(map.width()):
    if map.get_tile((x,0)) == '.':
      return (x,0)

def find_end_position(map):
  for x in range(map.width()):
    if map.get_tile((x,map.height()-1)) == '.':
      return (x,map.height()-1)

def fill_path(map,pos):
  free_path = None
  for d in directions.values():
    blocked = 0
    pos = (pos[0]+d[0],pos[1]+d[1])
    if map.get_tile(pos) == '#':
      blocked += 1
    else:
      free_path = pos
  if blocked == 3:
    print(pos, 'is blocked')
    map.set_tile(pos,'#')
    return 1 + fill_path(map,free_path)
  return 0

def cleanup_dead_ends(map):
  filled_tiles = 1
  while filled_tiles > 0:
    filled_tiles = 0
    for x in range(1,map.width()-1):
      for y in range(1,map.height()-1):
        if map.get_tile( (x,y) ) in ['>','<','^','v']:
          map.set_tile((x,y),'.')
        filled_tiles += fill_path(map, (x,y) )
  print(map)

def part2(map):
  print(map)
  cleanup_dead_ends(map) # There are no dead ends by design...
  paths = find_paths(map) 
  print('Longest path:', paths[-1].length)

def find_paths(map):
  s_pos = find_start_position(map)
  e_pos = find_end_position(map)
  paths = SortedList()
  paths.add( Path( s_pos ) )
  finished_paths = SortedList()
  while paths:
    p = paths.pop(0)
    if p.pos == e_pos:
      print('Length:', p.length)
      finished_paths.add(p)
    current_tile = map.get_tile(p.pos)
    possible_dirs = list(directions.values())
    for d in directions.values():
      pos = (p.pos[0]+d[0],p.pos[1]+d[1])
      if (not map.is_valid_pos(pos)) or \
          map.get_tile(pos) == '#' or \
          pos in p.history:
        possible_dirs.remove(d)
    if not possible_dirs:
      continue
    for dir in possible_dirs:
      q = p.copy()
      q.step(dir)
      q.record_step(len(possible_dirs))
      # Fork off
      paths.add( q )
  return finished_paths
  
map = Map('test.dat')
part2(map)