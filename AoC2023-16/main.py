import re
from collections import deque
from contextlib import suppress
from copy import deepcopy


class Map:
  
  def __init__(self, file_name = ''):
    if file_name:
      self.load_data(file_name)
    else:
      self.map_data = []

  def __repr__(self):
    return ''.join([''.join(row)+'\n' for row in self.map_data])
  
  def load_data( self, file_name ):
    with open(file_name,'r') as file:
      self.map_data = [ list(line.strip()) for line in file]

  def width(self):
    return len(self.map_data[0]) if len(self.map_data) > 0 else 0

  def height(self):
    return len(self.map_data)
      
  def fill_map(self, x, y, tile = '.'):
    self.map_data = [ [ tile for col in range(x) ] for row in range(y) ]

  def is_valid_pos(self,pos):
    return \
    (pos[1] >= 0 and pos[1] < len(self.map_data) and \
    pos[0] >= 0 and pos[0] < len(self.map_data[pos[1]]))

  def get_tile(self, pos):
    if not self.is_valid_pos(pos):
      raise IndexError
    return self.map_data[pos[1]][pos[0]]

  def set_tile(self,pos,tile):
    if not self.is_valid_pos(pos):
      raise IndexError
    self.map_data[pos[1]][pos[0]] = tile
    
  def find_tile(self, tile):
    for y, line in enumerate(self.map_data):
      with suppress(ValueError):
        return (line.index(tile),y)
    return (None,None)

  def count(self,tile):
    n = 0
    for line in self.map_data:
      n += line.count(tile)
    return n

class Mover:

  def __init__(self,p,d):
    self.set_pos(p)
    self.set_dir(d)

  def __repr__(self):
    return 'Mover: {}, {}'.format(self.pos, self.dir)

  def set_pos(self,p):
    self.pos = p
    
  def set_dir(self,d):
    if isinstance(d,str):
      match d:
        case 'N':
          self.dir = (0,-1)
        case 'S':
          self.dir = (0,1)
        case 'W':
          self.dir = (-1,0)
        case 'E':
          self.dir = (1,0)
        case _:
          raise ValueError('Invalid direction \'' + d + '\'')
    else:
      self.dir = (d[0],d[1])

  def step(self):
    self.set_pos((self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]))

def been_there( states, ray ):
  return ray.dir in states.get(ray.pos,[])

def energize(optical_map, ray):
  energy_map = Map()
  energy_map.fill_map( optical_map.width(), optical_map.height() )
  rays = deque([ray])
  visited_states = {}
  while rays:
    ray = rays.pop()
    while not been_there(visited_states,ray):
      visited_states.setdefault(ray.pos,[]).append(ray.dir)
      ray.step()
      with suppress(IndexError):
        energy_map.set_tile(ray.pos,'#')
      if not optical_map.is_valid_pos(ray.pos):
        break
      match optical_map.get_tile(ray.pos):
        case '\\':
          ray.set_dir( [ray.dir[1], ray.dir[0]])
        case '/':
          ray.set_dir( [-ray.dir[1], -ray.dir[0]])
        case '|':
          if ray.dir[0] != 0:
            ray.set_dir( [0, 1])
            rays.append( Mover( ray.pos, [0,-1] ))
        case '-':
          if ray.dir[1] != 0:
            ray.set_dir( [1, 0])
            rays.append( Mover( ray.pos, [-1,0] ))
        case '.':
          pass
        case _:
          raise ValueError('Unknown map tile')
  return energy_map.count('#')

def part1(map):
  print( 'Part1: ', energize(map,Mover((-1,0),'E')) )

def part2(map):
  w = map.width()
  h = map.height()
  energies = []
  for x in range(w):
    energies.append(energize(map,Mover((x,-1),'S')))
    energies.append(energize(map,Mover((x,h),'N')))
  for y in range(h):
    energies.append(energize(map,Mover((-1,y),'E')))
    energies.append(energize(map,Mover((w,y),'W')))
  print('Part2: ', max(energies))
  
map = Map('input.dat')
part1(map)
part2(map)