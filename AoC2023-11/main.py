with open('input.dat','r') as file:
  star_map = [list(line.strip()) for line in file]

def insert_col( rows, index, character):
  for row in rows:
    row.insert(index, character)

def fill_col( rows, index, character):
  for row in rows:
    row[index] = character

def fill_row( rows, index, character ):
  rows[index] = [character]*len(rows[index])

x = 0
while x < len(star_map[0]):
  if all( row[x] == '.' for row in star_map ):
    fill_col( star_map, x, '*' )
  x += 1
y = 0
while y < len(star_map):
  if all( x == '.' or x == '*' for x in star_map[y] ):
    fill_row( star_map, y, '*' )
  y += 1

galaxy_coords = []
y_coord = 0
inflation = 1000000
for y,row in enumerate(star_map):
  x_coord = 0
  for x, object in enumerate(row):
    if object == '#':
      galaxy_coords.append((x_coord,y_coord))
    x_coord += inflation if object == '*' else 1
  y_coord += inflation if row[0] == '*' else 1
      
sum = 0
for i1 in range(0, len(galaxy_coords) ):
  for i2 in range( i1 + 1, len(galaxy_coords) ):
    g1x, g1y = galaxy_coords[i1]
    g2x, g2y = galaxy_coords[i2]
    sum += abs(g1x - g2x) + abs(g1y - g2y)

print(sum)