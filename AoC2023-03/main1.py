# Imports string data line by line
data = [ line.rstrip() for line in open( 'input.dat', 'r' ) ]

ny = len(data)
nx = len(data[0])

def digits_to_int(digits):
  s = ''
  for d in digits:
    s += d
  return int(s)

def get_symbol(x,y, symbols):
  if x < 0 or x >= nx or y < 0 or y >= ny or data[y][x] == '.' or data[y][x].isdigit():
    return
  symbols.append(data[y][x])

def handle_start(x,y,symbols):
  get_symbol(x-1,y-1,symbols)
  get_symbol(x-1,y,symbols)
  get_symbol(x-1,y+1,symbols)

def handle_middle(x,y,symbols):
  get_symbol(x,y-1,symbols)
  get_symbol(x,y+1,symbols)

def handle_end(x,y,symbols, digits, pnums):
  get_symbol(x,y-1,symbols)
  get_symbol(x,y,symbols)
  get_symbol(x,y+1,symbols)
  if len(symbols) > 0:
    pnums.append(digits_to_int(digits))
    symbols.clear()
  digits.clear()

part_numbers = []
digits = []
symbols = []
for y, line in enumerate(data):
  for x, character in enumerate(line):
    if not character.isdigit():
      if digits:
        handle_end(x,y,symbols,digits,part_numbers)
      continue
    digits.append(character)
    # is first digit
    if len(digits) == 1:
      handle_start(x,y,symbols)
    handle_middle(x,y,symbols)
    # handle last number
    if x+1 == nx:
      handle_end(x,y,symbols,digits,part_numbers)

print(part_numbers)
print(sum(part_numbers))