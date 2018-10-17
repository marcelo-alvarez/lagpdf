import scipy as sp
import numpy as np
from scipy.spatial import *

def ReturnDistanceToNthNeighbor(pos,N):
    
    n=len(pos[:,0])
    posTree = cKDTree(pos)
    R=np.zeros(n)

    for i in np.arange(n):

        pi=pos[i]
        result = posTree.query(pi,k=N)

        # result [0][j] - distance to the j-th nearest neighbor of point i
        # result [1][j] - index    to the j-th nearest neighbor of point i

        R[i] = result[0][N-1]

    return R

n = 10000
N = 16

pos = np.zeros((n,3))

pos[:,0] = np.random.uniform(size=n)
pos[:,1] = np.random.uniform(size=n)
pos[:,2] = np.random.uniform(size=n)

rho = n
Rav = (3*N/4./np.pi/rho)**(1./3.)

buff = 2*Rav

p1 = buff
p2 = 1-buff

dm = [(pos[:,0]>p1) & (pos[:,0]<p2) &
      (pos[:,1]>p1) & (pos[:,1]<p2) &
      (pos[:,2]>p1) & (pos[:,2]<p2) ]

pos = pos[dm]

print pos[:,0].min(),pos[:,0].max()

R = ReturnDistanceToNthNeighbor(pos,N)
 
print ((R/Rav)**3).mean()








