import re
from collections import deque
from contextlib import suppress
from copy import deepcopy
from sortedcontainers import SortedList


def sign(x):
  return (x > 0) - (x < 0)
  
def load_data(file_name):
  convert = { '0':'R', '1':'D', '2':'L', '3':'U'}
  with open(file_name,'r') as file:
    data = [line.strip().split() for line in file]
  # Part 1
  #data = [ [dir, int(length)] for dir, length, _color in data ]
  # Part 2
  data = [color.strip('(#)') for dir, length, color in data]
  data = [ [convert[color[5]], int(color[0:5],16)] for color in data]
  for i, line in enumerate(data):
    if i == 0:
      line[0] = '0' + line[0] + data[i+1][0]
    elif i == len(data)-1:
      line[0] = data[i-1][0][1] + line[0] + '0'
    else:
      line[0] = data[i-1][0][1] + line[0] + data[i+1][0]
  data[0][0] = data[-1][0][1] + data[0][0][1:]
  data[-1][0] = data[-1][0][:2] + data[0][0][1]
  return data

def get_boundary(dig_plan):
  signs = {'U':-1, 'D':1, 'R':1, 'L':-1}
  vertical = ['U', 'D']
  horizontal = ['R', 'L']
  u_shaped = ['URD', 'DRU', 'ULD', 'DLU', 'RUL', 'LUR', 'RDL', 'LDR']
  ccw = ['UL', 'DR', 'RU', 'LD']
  x = 0
  y = 0
  coords = [(0,0)]
  n = (-1,0)
  for dir, length in dig_plan:
    if dir[:2] in ccw:
      n = (n[1],-n[0])
    else:
      n = (-n[1],n[0])
    if dir in u_shaped:
      if signs[dir[2]] == n[0]+n[1]:
        length -= 1
      else:
        length += 1
    if dir[1] in horizontal:
      x += length*signs[dir[1]]
    else:
      y += length*signs[dir[1]]
    coords.append( (x,y) )
  return coords

def calc_volume(coords):
  volume = 0
  x1 = 0
  y1 = 0
  for x0, y0 in coords:
    volume += (x1-x0)*y0
    x1 = x0
    y1 = y0
  return volume

dig_plan = load_data('input.dat')
coords = get_boundary(dig_plan)
volume = calc_volume(coords)
print(volume)