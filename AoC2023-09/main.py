import numpy as np

def extrapolate(seq):
  seqs = [np.append(np.insert(seq,0,0),0)]
  while seqs[-1][1:-1].any():
    s = seqs[-1]
    seqs.append( s[1:] - s[0:-1] )
  seqs[-1][0] = 0
  seqs[-1][-1] = 0
  for i in range( len(seqs)-1, 0, -1):
    seqs[i-1][0] = seqs[i-1][1] - seqs[i][0]
    seqs[i-1][-1] = seqs[i][-1] + seqs[i-1][-2]
  return seqs

data = [np.array(list(map(int,line.strip().split()))) for line in open('input.dat','r')]

extrapolated = [extrapolate(arr) for arr in data]

print( sum([e[0][0] for e in extrapolated]))