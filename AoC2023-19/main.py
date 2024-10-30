import re
from collections import deque
from contextlib import suppress
from copy import deepcopy
from sortedcontainers import SortedList


class Condition:
  
  def __init__(self,s):
    if s.count(':') == 1:
      match s[0]:
        case 'x':
          self.variable = 0
        case 'm':
          self.variable = 1
        case 'a':
          self.variable = 2
        case 's':
          self.variable = 3
      self.operator = s[1]
      tmp = s[1:].strip('<>=').split(':')
      self.value = int(tmp[0])
      self.destination = tmp[1]
    else:
      self.variable = None
      self.operator = None
      self.value = None
      self.destination = s
      
  def __repr__(self):
    v = ''
    match self.variable:
      case 0:
        v = 'x'
      case 1:
        v = 'm'
      case 2:
        v = 'a'
      case 3:
        v = 's'
      case None:
        return 'else -> {}'.format(self.destination)
    return '{} {} {} -> {}'.format(v, self.operator, self.value, self.destination)

  def apply(self,part):
    if self.variable is None:
      return self.destination
    if (self.operator == '>' and part[self.variable] > self.value) or \
    (self.operator == '<' and part[self.variable] < self.value):
      return self.destination
    return None

  def apply_range(self,pr):
    if self.variable is None:
      pr.destination = self.destination
      return pr, None
    r = pr.ranges[self.variable]
    if self.operator == '>':
      if r[0] > self.value:
        pr.destination = self.destination
        return pr, None
      if r[1] <= self.value:
        return None, pr
      pr1 = pr
      pr2 = pr.copy()
      pr1.ranges[self.variable][0] = self.value + 1
      pr1.destination = self.destination
      pr2.ranges[self.variable][1] = self.value
      return pr1, pr2
    if self.operator == '<':
      if r[1] < self.value:
        return pr, None
      if r[0] >= self.value:
        return None, pr
      pr1 = pr
      pr2 = pr.copy()
      pr1.ranges[self.variable][1] = self.value - 1
      pr1.destination = self.destination
      pr2.ranges[self.variable][0] = self.value
      return pr1, pr2

class Workflow:

  def __init__(self, name, conditions):
    self.name = name
    self.conditions = conditions

  def __repr__(self):
    c_str = ', '.join([c.__repr__() for c in self.conditions])
    return '{} [{}]'.format(self.name, c_str)

  def sort(self,part):
    for c in self.conditions:
      dest = c.apply(part)
      if dest:
        return dest

  def sort_range(self, pr):
    part_ranges = []
    for c in self.conditions:
      pr1, pr2 = c.apply_range(pr)
      if pr1:
        part_ranges.append(pr1)
      if pr2:
        pr = pr2
      else:
        break
    return part_ranges


class PartRange:

  def __init__(self, dest, ranges):
    self.destination = dest
    self.ranges = ranges

  def __repr__(self):
    return '@{} x: {}-{}, m: {}-{}, a: {}-{}, s: {}-{}'.format(self.destination, self.ranges[0][0], self.ranges[0][1], self.ranges[1][0], self.ranges[1][1], self.ranges[2][0], self.ranges[2][1], self.ranges[3][0], self.ranges[3][1])

  def copy(self):
    return deepcopy(self)

def sort_range(pr, workflows):
  part_ranges = []
  if pr.destination in ['A','R']:
    return [pr]
  for x in workflows[pr.destination].sort_range(pr):
    part_ranges.extend(sort_range(x, workflows))
  return part_ranges
  
def load_data(file_name):
  with open(file_name,'r') as file:
    data = [line.strip() for line in file]
  index = 0
  while data[index]:
    index += 1
  workflows = [ line.strip('}').split('{') for line in data[:index] ]
  workflows = { w[0]:Workflow(w[0],[Condition(c) for c in w[1].split(',')]) for w in workflows}
  parts = [[int(x.strip('xmas')) for x in y] for y in [re.sub('[=\{\}]','',line).split(',') for line in data[index+1:] ] ]
  return workflows, parts

def count_combinations(part_ranges):
  combinations = 0
  for pr in [ pr for pr in part_ranges if pr.destination == 'A']:
    c = 1
    for r in pr.ranges:
      n = r[1]-r[0] + 1
      c *= n
    combinations += c
  return combinations

def part1(workflows, parts):
  acceptance = 0
  for part in parts:
    destination = 'in'
    while destination not in ['A', 'R']:
      destination = workflows[destination].sort(part)
    if destination == 'A':
      for i in range(4):
        acceptance += part[i]
  return acceptance

def part2(workflows):
  pr = PartRange('in',[[1,4000],[1,4000],[1,4000],[1,4000]])
  part_ranges = sort_range(pr, workflows)
  return count_combinations( part_ranges )

workflows, parts = load_data('input.dat')
  
#print('Part 1:',part1(workflows,parts))

print( 'Part 2:', part2(workflows) )