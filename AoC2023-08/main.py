import math

data = [line.strip() for line in open('input.dat','r')]

instructions = data[0]

junctions = {}
for intersections in data[2:]:
  current_node, destination_nodes = intersections.split(' = ')
  l_node, r_node = destination_nodes.strip(' ()').split(',')
  junctions[current_node] = (l_node.strip(), r_node.strip())

# Part 1
#path = ['AAA']
#i = 0
#while path[-1] != 'ZZZ':
#  path.append( junctions[path[-1]][0 if instructions[i] == 'L' else 1] )
#  i += 1
#  if i == len(instructions):
#    i = 0
#print(len(path)-1)

# Part 2
paths = []
for j in junctions:
  if j[-1] == 'A':
    paths.append([0,j, None, None, None])
    # 0: Steps from start
    # 1: Current loc
    # 2: Loop start loc
    # 3: Period
    # 4: Character index

for path in paths:
  cycle_found = False
  while not cycle_found:
    for i, dir in enumerate(instructions):
      path[1] = junctions[path[1]][0 if dir == 'L' else 1]
      path[0] += 1
      if path[2] == path[1] and path[4] == i:
        path[3] = path[0] - path[3]
        cycle_found = True
        break
      elif path[2] is None and path[1][-1] == 'Z':
        path[2] = path[1]
        path[3] = path[0]
        path[4] = i

# All cycles start with the first letter and are a multiple of the number of instructions long, therefor the answer is the lowest common multiple of all the periods.
print(math.lcm(*[path[3] for path in paths]))