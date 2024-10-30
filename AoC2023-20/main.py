import re
from collections import deque
from contextlib import suppress
from copy import deepcopy
from math import lcm
from sortedcontainers import SortedList

class Signal:
  def __init__(self,sender,dest,value,generation):
    self.sender = sender
    self.dest = dest
    self.value = value
    self.gen = generation
  def __repr__(self):
    return '[{}] {} -> {} (gen: {})'.format(self.value,self.sender,self.dest,self.gen)

class SignalException(Exception):
  def __init__(self,periods):
    self.periods = periods

class Module:
  def __init__(self, type, name, destinations):
    self.type = type
    self.name = name
    self.dest = destinations
  def __repr__(self):
    return '{} ({}) -> {}'.format(self.name, self.type, self.dest)
  def activate(self, signal):
    signals = []
    for d in self.dest:
      signals.append( Signal(self.name,d,signal.value,signal.gen) )
    return signals

class Button(Module):
  def __init__(self,name):
    Module.__init__(self,'bt',name,['broadcaster'])
  def activate(self,generation):
    return Module.activate(self, Signal('','button',0,generation))
    
class Broadcaster(Module):
  def __init__(self,name,destinations):
    Module.__init__(self,'bc',name,destinations)

class Output(Module):
  def __init__(self,name):
    Module.__init__(self,'op',name,[])
    
class FlipFlop(Module):
  def __init__(self,name,destinations):
    Module.__init__(self,'ff',name,destinations)
    self.state = False
  def __repr__(self):
    state = ' (On)' if self.state else ' (Off)'
    return Module.__repr__(self) + state
  def activate(self, signal):
    if signal.value != 0:
      return []
    self.state = not self.state
    signal.value = 1 if self.state else 0
    return Module.activate(self, signal)
    
class Conjunction(Module):
  def __init__(self,name,destinations):
    Module.__init__(self,'cj',name,destinations)
    self.inputs = {}
    self.periods = {}
    self.confirmed_periods = {}
    self.last_high = {}
  def __repr__(self):
    state = ' ' + str(self.inputs)
    return Module.__repr__(self) + state
  def activate(self,signal):
    self.inputs[signal.sender] = signal.value
    if self.name =='zh' and signal.value == 1:
      old_period = self.periods.get(signal.sender,0)
      new_period = signal.gen - self.last_high.get(signal.sender,0)
      if old_period == new_period:
        self.confirmed_periods[signal.sender] = old_period
        if self.periods == self.confirmed_periods:
          raise SignalException(self.confirmed_periods)
      else:
        self.periods[signal.sender] = new_period
        self.last_high[signal.sender] = signal.gen
    signal.value = 0 if all( input == 1 for input in self.inputs.values()) else 1
    return Module.activate(self,signal)
    
  def register_inputs(self,modules):
    for m in modules:
      if self.name in m.dest:
        self.inputs[m.name] = 0

def load_data(file_name):
  with open(file_name,'r') as file:
    data = [line.strip().split(' -> ') for line in file]
  modules = {}
  for name, destinations in data:
    destinations = [ d.strip() for d in destinations.split(',')]
    if name == 'broadcaster':
      modules[name] = Broadcaster(name,destinations) 
    else:
      match name[0]:
        case '%':
          name = name[1:]
          modules[name] = FlipFlop(name,destinations) 
        case '&':
          name = name[1:]
          modules[name] = Conjunction(name,destinations) 
        case _:
          print('Unknown module type:', name[0])
  modules['button'] = Button('button')
  for m in modules.values():
    if m.type == 'cj':
      m.register_inputs(modules.values())
  return modules

def push_button(modules,generation=0):
  #print('Pushing button')
  signals = deque( modules['button'].activate(generation) )
  n_low = 0
  n_high = 0
  while signals:
    signal = signals.popleft()
    if signal.value == 0:
      n_low += 1
    else:
      n_high += 1
    [signals.append(s) for s in modules.setdefault(signal.dest,Output(signal.dest)).activate(signal)]
  return n_low, n_high

def part1():
  mods = load_data('input.dat')
  n_tot = [0,0]
  for _ in range(1000):
    n = push_button(mods)
    n_tot[0] += n[0]
    n_tot[1] += n[1]
  return n_tot[0]*n_tot[1]

def part2():
  mods = load_data('input.dat')
  pushes = 0
  while True:
    pushes += 1
    try:
      push_button(mods, pushes)
    except SignalException as e:
      return lcm(*e.periods.values())

print('Part 1:', part1())
print('Part 2:', part2())