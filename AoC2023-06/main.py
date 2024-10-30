from math import sqrt
from math import floor
from math import ceil

# Imports string data line by line
data = [line.rstrip() for line in open('input.dat', 'r')]

races = list(zip([ int(t) for t in data[0].split(':')[1].strip().split()],[int(d) for d in data[1].split(':')[1].strip().split()] ) )

def ways_of_winning( race ):
  tot_time, min_dist = race
  t_max = tot_time / 2 + sqrt(tot_time*tot_time/4-min_dist)
  if t_max == floor(t_max):
    t_max -= 1
  t_max = floor(t_max)
  t_min = tot_time / 2 - sqrt(tot_time*tot_time/4-min_dist)
  if t_min == ceil(t_min):
    t_min += 1
  t_min = ceil(t_min)
  return (t_max - t_min) + 1

# Part 1
ways = 1
for r in races:
  ways *= ways_of_winning(r)

print(ways)

# Part 2

time = int(''.join(data[0].split(':')[1].strip().split()))
dist = int(''.join(data[1].split(':')[1].strip().split()))

print( ways_of_winning([time,dist]))