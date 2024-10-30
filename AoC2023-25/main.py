from copy import deepcopy
from collections import deque


def load_data(filename):
  data = {}
  with open(filename,'r') as file:
    for line in file:
      component, connections = line.split(': ')
      data[component] = connections.split()
  return data

def write_graphviz_file(filename, connections):
  with open(filename, 'w') as out:
    out.write('strict graph Diagram {\n')
    for a, connections in connections.items():
      out.write('{:s} -- {{{:s}}}\n'.format(a,','.join(connections)))
    out.write('}')

def fill_dict(edges):
  edges2 = deepcopy(edges)
  for node, connections in edges.items():
    for c in connections:
      edges2.setdefault(c,[]).append(node)
  edges2['fzb'].remove('fxr') 
  edges2['fxr'].remove('fzb')
  edges2['nmv'].remove('thl') 
  edges2['thl'].remove('nmv')
  edges2['vgk'].remove('mbq') 
  edges2['mbq'].remove('vgk')
  return edges2
  
def count_nodes(edges):
  visited = {}
  for node, connections in edges.items():
    visited[node] = False

  start_node = next(iter(edges))
  to_visit = deque()
  to_visit.append(start_node)
  visited[start_node] = True
  n = 0
  while to_visit:
    node = to_visit.pop()
    connections = edges[node]
    n += 1
    for c in connections:
      if not visited[c]:
        to_visit.append(c)
        visited[c] = True
  return n

edges = load_data('input.dat')
write_graphviz_file('graph.dot', edges)
edges = fill_dict( edges )
n1 = count_nodes(edges)
n2 = len(edges) - n1
print('Part 1:', n1*n2 )
# The three connections are 
# fzb -- fxr
# nmv - thl
# vgk - mbq
# identified just by viewing the dot file