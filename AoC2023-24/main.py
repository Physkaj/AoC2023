import numpy as np
from copy import deepcopy


np.set_printoptions(linewidth=np.inf)

class Trajectory:
  def __init__(self,pos,vel,dt=np.float64):
    self.p = np.array(pos,dtype=dt)
    self.v = np.array(vel,dtype=dt)
  def __repr__(self):
    return 'p:{} v:{}'.format(self.p,self.v)
  def x(self):
    return self.p[0]
  def y(self):
    return self.p[1]
  def z(self):
    return self.p[2]
  def vx(self):
    return self.v[0]
  def vy(self):
    return self.v[1]
  def vz(self):
    return self.v[2]
    
  def calc_pos(self,t):
    return self.p+self.v*t
    
  def closest_approach(tr1,tr2):
    delta_v = tr2.v - tr1.v
    delta_x = tr2.p - tr1.p
    D = delta_x - delta_v*np.dot(delta_v,delta_x) / np.dot(delta_v,delta_v)
    return D.dot(D)

def load_data(filename):
  vectors = []
  with open(filename,'r') as input:
    data = [ line.strip().split('@') for line in input]
    for p, v in data:
      p = [int(pos) for pos in p.strip().split(',')]
      v = [int(vel) for vel in v.strip().split(',')]
      vectors.append(Trajectory(p,v))
  return vectors

def part2(trajectories):
  def rms(tr1):
    rms = 0
    for tr2 in trajectories:
      rms += Trajectory.closest_approach(tr1,tr2)
    #rms /= len(trajectories)
    #return np.sqrt(rms)
    return rms
  
  matrix = np.zeros((6,6))
  tr0 = trajectories[0]
  tr1 = trajectories[1]
  tr2 = trajectories[2]
  matrix[0][1] = tr0.vz()-tr1.vz()
  matrix[0][2] = tr1.vy()-tr0.vy()
  matrix[0][4] = tr1.z() - tr0.z()
  matrix[0][5] = tr0.y() - tr1.y()
  matrix[1][0] = tr1.vz()-tr0.vz()
  matrix[1][2] = tr0.vx()-tr1.vx()
  matrix[1][3] = tr0.z() - tr1.z()
  matrix[1][5] = tr1.x() - tr0.x()
  matrix[2][0] = tr0.vy()-tr1.vy()
  matrix[2][1] = tr1.vx()-tr0.vx()
  matrix[2][3] = tr1.y() - tr0.y()
  matrix[2][4] = tr0.x() - tr1.x()

  matrix[3][1] = tr0.vz()-tr2.vz()
  matrix[3][2] = tr2.vy()-tr0.vy()
  matrix[3][4] = tr2.z() - tr0.z()
  matrix[3][5] = tr0.y() - tr2.y()
  matrix[4][0] = tr2.vz()-tr0.vz()
  matrix[4][2] = tr0.vx()-tr2.vx()
  matrix[4][3] = tr0.z() - tr2.z()
  matrix[4][5] = tr2.x() - tr0.x()
  matrix[5][0] = tr0.vy()-tr2.vy()
  matrix[5][1] = tr2.vx()-tr0.vx()
  matrix[5][3] = tr2.y() - tr0.y()
  matrix[5][4] = tr0.x() - tr2.x()
  ordinates = np.array([ \
    tr0.y()*tr0.vz() - tr0.z()*tr0.vy() - tr1.y()*tr1.vz() + tr1.z()*tr1.vy(), \
    tr0.z()*tr0.vx() - tr0.x()*tr0.vz() - tr1.z()*tr1.vx() + tr1.x()*tr1.vz(), \
    tr0.x()*tr0.vy() - tr0.y()*tr0.vx() - tr1.x()*tr1.vy() + tr1.y()*tr1.vx(), \
    tr0.y()*tr0.vz() - tr0.z()*tr0.vy() - tr2.y()*tr2.vz() + tr2.z()*tr2.vy(), \
    tr0.z()*tr0.vx() - tr0.x()*tr0.vz() - tr2.z()*tr2.vx() + tr2.x()*tr2.vz(), \
    tr0.x()*tr0.vy() - tr0.y()*tr0.vx() - tr2.x()*tr2.vy() + tr2.y()*tr2.vx(), \
  ])
  solution = np.linalg.solve(matrix,ordinates)

  # Solution is not exact, look for integers
  best = 1000
  best_stone = None
  for x in range(-2,3):
    for y in range(-2,3):
      for z in range(-2,3):
        delta = np.array([x,y,z])
        stone = Trajectory(np.round(solution[:3])+delta, np.round(solution[3:]), np.int64)
        d = rms(stone)
        if d < best:
          best = d
          best_stone = stone
  return np.sum(best_stone.p)
  

test = load_data('test.dat')
real = load_data('input.dat')
print('Test 2:',part2(test))
print('Part 2:',part2(real))
    