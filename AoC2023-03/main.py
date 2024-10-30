# Imports string data line by line
data = [line.rstrip() for line in open('test2.dat', 'r')]

ny = len(data)
nx = len(data[0])


class Symbol:

  def __init__(self, x, y, s):
    self.x = x
    self.y = y
    self.symbol = s

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return '({x}, {y}): {symb}'.format(x=self.x, y=self.y, symb=self.symbol)

  def number(self):
    return int(self.symbol)

def find_numbers(data):
  numbers = {}
  s = ''
  x_start = 0
  for y, line in enumerate(data):
    for x, c in enumerate(line):
      if c.isdigit():
        if not s:
          x_start = x
        s += c
      if (not c.isdigit() and s) or (c.isdigit() and x == len(line)-1):
        numbers.setdefault(y, []).append(Symbol(x_start, y, s))
        s = ''
  return numbers


def find_symbols(data, symbol_str):
  symbols = {}
  for y, line in enumerate(data):
    for x, c in enumerate(line):
      if c in symbol_str:
        symbols.setdefault(y, []).append(Symbol(x, y, c))
  return symbols


numbers = find_numbers(data)
print(numbers)
symbols = find_symbols(data, '*')
print(symbols)

gear_ratios = []
for slist in symbols.values():
  for s in slist:
    neighbours = []
    for line in range(max(0, s.y - 1), min(len(data), s.y + 2)):
      for num in numbers.get(line, []):
        if not (num.x + len(num.symbol) - 1 < s.x - 1 or num.x > s.x + 1):
          neighbours.append(num.number())
    if len(neighbours) == 2:
      gear_ratios.append(neighbours[0] * neighbours[1])

print(sum(gear_ratios))
