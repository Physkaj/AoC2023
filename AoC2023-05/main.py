# Imports string data line by line
data = [line.rstrip() for line in open('input.dat', 'r')]

seed_data = [int(s) for s in data[0].split(':')[1].split()]
maps = []
for line in data[2:]:
  if line == '':
    continue
  index = line.find(' map:')
  if index == -1:
    maps[-1].append( tuple(int(x) for x in line.split() ) )
    continue
  maps.append([])

def map_it( map_level, input ):
  if map_level >= len(maps):
    return [input]
  for m in maps[map_level]:
    dest_start = m[0]
    source_start = m[1]
    range = m[2]
    range1 = 0
    range2 = 0
    if source_start <= input[0] < source_start + range:
      # Starting point is inside the map range
      if source_start <= input[0]+input[1]-1 < source_start + range:
        # End point is also inside the map range
        interval = [dest_start + (input[0] - source_start), input[1] ]
        return map_it(map_level+1, interval)
      # End point is outside the map range
      range1 = source_start + range - input[0]
      range2 = input[1] - range1
    elif source_start <= input[0] + input[1] - 1 < source_start + range:
      # Ending point is inside the map range but starting point is not
      range1 = source_start - input[0]
      range2 = input[1] - range1
    if range1 > 0:
      interval1 = [input[0], range1]
      interval2 = [input[0] + range1, range2]
      return map_it(map_level, interval1) + map_it(map_level,interval2)
  return map_it( map_level + 1, input )
#location = 0
#while map_location_to_seed(location) not in seed_data:
#  location += 1
#print(location, map_location_to_seed(location))

#locations = [ map_seed_to_location(s) for s in seed_data]
#print(locations)

seeds = [ (seed_data[i], seed_data[i+1]) for i in range(0,len(seed_data),2)]
print(seeds)

locations = []
for s in seeds:
  locations += map_it(0,s)

print(min(locations))
