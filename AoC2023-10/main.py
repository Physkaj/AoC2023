with open('input.dat','r') as file:
  pipe_map =[list(line.strip()) for line in file]

def get_tile(pos,data):
  if pos[1] < 0 or pos[1] >= len(data) or pos[0] < 0 or pos[0] > len(data[pos[1]]):
    return ' '
  return data[pos[1]][pos[0]]

def set_tile(pos,data, tile):
  if pos[1] < 0 or pos[1] >= len(data) or pos[0] < 0 or pos[0] > len(data[pos[1]]):
    return
  data[pos[1]][pos[0]] = tile

def find_tile(tile,data):
  for y, line in enumerate(data):
    if tile in line:
      return (line.index(tile),y)
  return -1

def find_starting_pipe_connections(start,data):
  pipes = []
  if get_tile(step(start,'N'),data) in '|F7':
    pipes.append('N')
  if get_tile(step(start,'S'),data) in '|JL':
    pipes.append('S')
  if get_tile(step(start,'E'),data) in '-J7':
    pipes.append('E')
  if get_tile(step(start,'W'),data) in '-FL':
    pipes.append('W')
  if len(pipes) != 2:
    print('Wrong number of starting pipe connections!')
  return pipes

def step(pos,dir):
  match dir:
    case 'N':
      return (pos[0],pos[1]-1)
    case 'S':
      return (pos[0],pos[1]+1)
    case 'E':
      return (pos[0]+1,pos[1])
    case 'W':
      return (pos[0]-1,pos[1])
    case '':
      return pos

def next_position(pos, dir, data):
  next_dir = ''
  match get_tile(pos, data):
    case '|':
      match dir:
        case 'N':
          next_dir = 'N'
        case 'S':
          next_dir = 'S'
    case '-':
      match dir:
        case 'E':
          next_dir = 'E'
        case 'W':
          next_dir = 'W'
    case 'L':
      match dir:
        case 'S':
          next_dir = 'E'
        case 'W':
          next_dir = 'N'
    case 'J':
      match dir:
        case 'E':
          next_dir = 'N'
        case 'S':
          next_dir = 'W'
    case '7':
      match dir:
        case 'E':
          next_dir = 'S'
        case 'N':
          next_dir = 'W'
    case 'F':
      match dir:
        case 'N':
          next_dir = 'E'
        case 'W':
          next_dir = 'S'
    case 'S':
      next_dir = dir
  return (step(pos,next_dir), next_dir)

s_to_pipe_map = {'NS':'|', 'NW': 'J', 'EN': 'L', 'SW': '7', 'ES': 'F', 'EW': '-'}
def determine_starting_pipe(pipes):
  return s_to_pipe_map[''.join(sorted(pipes))]

start = find_tile('S',pipe_map)
# Find the two start directions
pipes = find_starting_pipe_connections(start,pipe_map)

steps = 0
pos = start
dir = pipes[0]
pipe_mask = [ [False]*len(line) for line in pipe_map]

while True:
  pos, dir = next_position(pos, dir, pipe_map)
  steps += 1
  set_tile( pos, pipe_mask, True)
  if get_tile(pos,pipe_map) == 'S':
    break

print('Furthest distance: ', steps/2)

set_tile(start, pipe_map, determine_starting_pipe(pipes))
io_map = [ ['#']*len(line) for line in pipe_map]
for y, line in enumerate(pipe_mask):
  inside = False
  bend = ''
  for x, is_main_pipe in enumerate(line):
    pos = (x,y)
    if is_main_pipe:
      # A full vertical crossing is either |, L7 or FJ
      tile = get_tile(pos, pipe_map)
      match tile:
        case '-':
          continue 
        case '|':
          inside = not inside
        case _:
          bend += tile
          if len(bend) == 2:
            if bend == 'L7' or bend == 'FJ':
              inside = not inside
            bend = ''
    else:
      set_tile( pos, io_map, 'I' if inside else 'O')

tiles_inside = 0
for line in io_map:
  tiles_inside += line.count('I')
print('Tiles inside: ', tiles_inside)