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
  def __init__(self,start_node):
    self.nodes = {start_node:0}

  def __repr__(self):
    s = 'Length: {}, start: {}, end: {}\n'.format( \
      self.length() , self.first_node(), self.last_node())
    s += 'History:\n'
    tot_dist = 0
    for node, dist in self.nodes.items():
      tot_dist += dist
      s+= '->{} [{}]\n'.format(node,tot_dist)
    return s

  def __eq__(self,other):
    return self.nodes == other.nodes

  def __gt__(self,other):
    return self.length() > other.length()

  def first_node(self):
    return next(iter(self.nodes))

  def last_node(self):
    return next(reversed(self.nodes))

  def length(self):
    total = 0
    for dist in self.nodes.values():
      total += dist
    return total

def find_start_node(map):
  for x in range(map.width()):
    if map.get_tile((x,0)) == '.':
      return (x,0)

def find_end_node(map):
  for x in range(map.width()):
    if map.get_tile((x,map.height()-1)) == '.':
      return (x,map.height()-1)

def count_surrounding_trees(map, pos):
  trees = 0
  for d in directions.values():
    trees += 1 if map.get_tile((pos[0]+d[0],pos[1]+d[1])) == '#' else 0
  return trees

def find_nodes(map):
  nodes = {find_start_node(map):0}
  for x in range(1,map.width()-1):
    for y in range(1,map.height()-1):
      if map.get_tile((x,y)) == '.' and count_surrounding_trees(map, (x,y) ) < 2:
        nodes[(x,y)] = 0
  nodes[find_end_node(map)] = 0
  return nodes

def remove_slopes(map):
  for x in range(1,map.width()-1):
    for y in range(1,map.height()-1):
      tile = map.get_tile((x,y))
      if tile in ['<','>','^','v']:
        map.set_tile((x,y),'.')

def travel_edge( map, nodes, history ):
  pos = history[-1]
  if pos in nodes:
    return (1,pos)
  for d in directions.values():
    new_pos = (pos[0]+d[0],pos[1]+d[1])
    if new_pos == history[-2] or map.get_tile(new_pos) == '#':
      continue
    history.append(new_pos)
    dist, dest = travel_edge(map,nodes,history)
    return (1 + dist, dest)

def find_edges(map,nodes):
  edges = {}
  for node in nodes:
    for d in directions.values():
      pos = (node[0]+d[0],node[1]+d[1])
      if not map.is_valid_pos(pos) or map.get_tile(pos) == '#':
        continue
      distance, destination = travel_edge(map, nodes, [node, pos])
      edges.setdefault(node,{})[destination] = distance
  return edges

def reduce_graph(edges):
  restart = True
  while restart:
    restart = False
    for node, connections in edges.items():
      if len(connections) != 3:
        continue
      i = iter(connections.items())
      node1, dist1 = next(i)
      node2, dist2 = next(i)
      node3, dist3 = next(i)
      del edges[node]
      del edges[node1][node], edges[node2][node], edges[node3][node]
      edges[node1][node2] = dist1+dist2
      edges[node1][node3] = dist1+dist3
      edges[node2][node1] = dist1+dist2
      edges[node2][node3] = dist2+dist3
      edges[node3][node1] = dist1+dist3
      edges[node3][node2] = dist2+dist3
      restart = True
      break
  return edges

def write_graphviz_file(edges,filename):
  with open(filename, 'w') as out:
    out.write('strict graph Diagram {{\n')
    for n, connections in edges.items():
      for c,d in connections.items():
        out.write('"{:s}" -- "{:s}" [label={}]\n'.format(str(n),str(c),d))
    out.write('}}')
      
def part2(map):
  remove_slopes(map)
  nodes = find_nodes(map)
  edges = find_edges(map,nodes)
  edges = reduce_graph(edges)
  #write_graphviz_file(edges,'output.dot')
  paths = find_paths(edges)
  print('Longest path:', paths[-1].length() )

def find_paths(edges):
  paths = deque()
  paths.append( Path( next(iter(edges)) ) )
  
  finished_paths = SortedList()
  while paths:
    p = paths.pop()
    if p.last_node() == next(reversed(edges)):
      finished_paths.add(p)

    for dest, dist in edges[p.last_node()].items():
      if dest in p.nodes:
        continue
      q = deepcopy(p)
      q.nodes[dest] = dist
      # Fork off
      paths.append( q )
  return finished_paths
  
map = Map('input.dat')
part2(map)