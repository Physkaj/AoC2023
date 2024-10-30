import copy

def arrange_data(data):
  return data

def load_data( file_name ):
  with open(file_name,'r') as file:
    data = [ list(line.strip()) for line in file]
  return arrange_data(data)

class Data:
  def __init__(self,d):
    self.data = d
  def __repr__(self):
    return ''.join([ ''.join(row)+'\n' for row in self.data])
  def to_string(self):
    return ''.join([ ''.join(row)+'\n' for row in self.data])
  def copy(self):
    return Data(copy.deepcopy(self.data))
  def size(self):
    return (self.x_size(), self.y_size())
  def x_size(self):
    return len(self.data[0])
  def y_size(self):
    return len(self.data)
  def get_item(self,coord):
    return self.data[coord[1]][coord[0]]
  def set_item(self,coord,item):
    self.data[coord[1]][coord[0]] = item
  def swap_items( self, coord1, coord2 ):
    item = self.get_item(coord1)
    self.set_item(coord1, self.get_item(coord2) )
    self.set_item(coord2, item)
  def slide(self,coord1,direction):
    coord2 = (coord1[0] + direction[0], coord1[1] + direction[1])
    if self.get_item(coord1) != 'O' or coord2[0] < 0 or \
    coord2[0] >= self.x_size() or coord2[1] < 0 or \
    coord2[1] >= self.y_size():
      return
    if self.get_item(coord2) == '.':
      self.swap_items(coord1, coord2)
      self.slide(coord2,direction)
  def get_load(self):
    load = 0
    for y, line in enumerate(self.data):
      load += sum(1 for item in line if item == 'O') * \
      (self.y_size() - y)
    return load
  def equals(self,other):
    #return all( item1 == item2 for item1, item2 in [line for line in zip(self.data, other.data,strict=True)])
    for x in range(0,self.x_size()):
      for y in range(0,self.y_size()):
        if self.get_item((x,y)) != other.get_item((x,y)):
          return False
    return True
  def tilt(self,n_cycles):
    old_data = {}
    cycles_performed = 0
    while cycles_performed < n_cycles:
      old_data[self.to_string()] = cycles_performed
      for x in range(0,self.x_size()):
        for y in range(0,self.y_size()):
          self.slide((x,y),(0,-1))
      for x in range(0,self.x_size()):
        for y in range(0,self.y_size()):
          self.slide((x,y),(-1,0))
      for x in range(self.x_size()-1,-1,-1):
        for y in range(self.y_size()-1,-1,-1):
          self.slide((x,y),(0,1))
      for x in range(self.x_size()-1,-1,-1):
        for y in range(self.y_size()-1,-1,-1):
          self.slide((x,y),(1,0))
      cycles_performed += 1
      old_cycles = old_data.get( data.to_string(), None)
      if old_cycles:
        period = cycles_performed - old_cycles
        cycles_left = n_cycles - cycles_performed
        cycles_performed += (cycles_left // period) * period
        print('Period: {}, old: {}, current: {}, cycles left: {}'.format(period,old_cycles,cycles_performed,cycles_left))

data = Data( load_data('input.dat'))
data.tilt(1000000000)
print('Load:', data.get_load())