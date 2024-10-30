from copy import deepcopy
from collections import deque


def load_data( file_name ):
  with open(file_name,'r') as file:
    data = [ [ [int(x) for x in brick.split(',')] for brick in line.strip().split('~')] for line in file]
  return data

class Brick:
  def __init__(self, ends ):
    self.begin = [0]*3
    self.end = [0]*3
    self.dir = 2
    for i in range(3):
      self.begin[i] = min(ends[0][i], ends[1][i]+1)
      self.end[i] = max(ends[0][i], ends[1][i]+1)
    self.supports = set()
    self.supported_by = set()
    self.__hash = hash( tuple(self.begin + self.end) )

  def __hash__(self):
    return self.__hash
  
  def __repr__(self):
    return '{} - {}'.format(self.begin, self.end)

  def __eq__(self, other):
    return self.__hash == other.__hash

  def __gt__(self, other):
    self_min_z = min(self.begin[2], self.end[2])
    other_min_z = min(other.begin[2], other.end[2])
    return self.bottom() > other.bottom() if \
      self.bottom() != other.bottom() else \
      self.height() > other.height()

  def bottom(self):
    return self.begin[2]

  def top(self):
    return self.end[2]

  def height(self):
    return self.end[2] - self.begin[2]

  def projections_overlap( b1, b2, axis = 2):
    d1 = 0 if axis != 0 else 1
    d2 = 2 if axis != 2 else 1
    return b1.begin[d1] < b2.end[d1] and b1.end[d1] > b2.begin[d1] and \
           b1.begin[d2] < b2.end[d2] and b1.end[d2] > b2.begin[d2]

  def overlap(b1, b2):
    return b1.begin[0] < b2.end[0] and b1.end[0] > b2.begin[0] and \
           b1.begin[1] < b2.end[1] and b1.end[1] > b2.begin[1] and \
           b1.begin[2] < b2.end[2] and b1.end[2] > b2.begin[2]

  def translate(self, vector):
    for axis in range(3):
      self.begin[axis] += vector[axis]
      self.end[axis] += vector[axis]
    
  def is_redundant(self):
    return all( len(b.supported_by) > 1 for b in self.supports)

  def collapse(self, collapsing = None ):
    if collapsing is None:
      collapsing = set()
    collapsing.add(self)
    for b in self.supports:
      if not (b.supported_by - collapsing):
        b.collapse(collapsing)
    return len(collapsing) - 1

class Wall:
  def __init__(self,bricks):
    self.bricks = deque(sorted(bricks))

  def __repr__(self):
    return '\n'.join([str(b) for b in self.bricks])

  def resort(self, brick, index):
    while index > 0 and self.bricks[index-1] > brick:
      index -= 1
    while index+1 < len(self.bricks) and self.bricks[index+1] < brick:
      index += 1
    self.bricks.remove(brick)
    self.bricks.insert(index, brick)
    
  def engage_gravity(self):
    falling_bricks = 0
    for i1 in range(len(self.bricks)):
      b1 = self.bricks[i1]
      max_fall_dist = b1.bottom()
      for i2 in range(i1):
        b2 = self.bricks[i2]
        if b1.bottom() == b2.bottom():
          break
        if b1.bottom() < b2.top():
          continue
        if Brick.projections_overlap(b1,b2,axis=2):
          max_fall_dist = min(b1.bottom() - b2.top(), max_fall_dist)
      if max_fall_dist > 0:
        falling_bricks += 1
        b1.translate( [0,0,-max_fall_dist])
        self.resort(b1,i1)
    self.update_support()
    return falling_bricks

  def update_support(self):
    for i1 in range(len(self.bricks)):
      b1 = self.bricks[i1]
      for i2 in range(i1+1,len(self.bricks)):
        b2 = self.bricks[i2]
        if b2.bottom() > b1.top():
          break
        if b2.bottom() == b1.top() and \
        Brick.projections_overlap(b1,b2,axis=2):
          # b2 is supported by b1
          b1.supports.add(b2)
          b2.supported_by.add(b1)

def part1(brick_data):
  bricks = []
  for d in data:
    bricks.append(Brick(d))
  wall = Wall(bricks)
  wall.engage_gravity()
  count = 0
  for b in wall.bricks:
    count += 1 if b.is_redundant() else 0
  return count

def part2(brick_data):
  bricks = []
  for d in data:
    bricks.append(Brick(d))
  wall = Wall(bricks)
  wall.engage_gravity()
  count = 0
  for b in wall.bricks:
    count += b.collapse()
  return count
    
data = load_data('input.dat')
#print('Part 1:', part1(data))
print('Part 2:', part2(data))