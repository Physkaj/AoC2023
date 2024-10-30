# Imports string data line by line
data = [ line.rstrip() for line in open( 'input.dat', 'r' ) ]

cube_limits = { 'red': 12, 'green': 13, 'blue': 14}

def cubes_in_color(color_data):
  color_data = color_data.strip()
  number_of_cubes, color = color_data.split(' ')
  return [color, int(number_of_cubes)]

def cubes_used_in_reveal(reveal_data):
  return [cubes_in_color(color_data) for color_data in reveal_data.split(',')]

def count_cubes_used_in_game(game_data):
  game_header, cube_data = game_data.split(':')
  game_number = int(game_header[5:])

  return game_number, [ cubes_used_in_reveal(cube_reveals) for cube_reveals in cube_data.split(';')]

cubes_used_in_games = [ count_cubes_used_in_game( game_data ) for game_data in data]

possible_games = []
for game_number, game_data in cubes_used_in_games:
  max_number_of_cubes = {}
  for reveal_data in game_data:
    for color, number_of_cubes in reveal_data:
      max_number_of_cubes[color] = max(max_number_of_cubes.get(color, 0), number_of_cubes)
    possible = True
    for color in cube_limits:
      if cube_limits[color] < max_number_of_cubes.get(color,0):
        possible = False
        break
  if possible:
    possible_games.append(game_number)

print('Possible game sum: ', sum(possible_games))

powers = []
for game_number, game_data in cubes_used_in_games:
  max_number_of_cubes = {}
  for reveal_data in game_data:
    for color, number_of_cubes in reveal_data:
      max_number_of_cubes[color] = max(max_number_of_cubes.get(color, 0), number_of_cubes)
  powers.append(max_number_of_cubes.get('red',0) * max_number_of_cubes.get('green',0) * max_number_of_cubes.get('blue',0))

print( sum(powers) )
  