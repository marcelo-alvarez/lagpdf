import numpy as np
import matplotlib.pyplot as plt
from parameters import *

npart = 1024.**3

if uniform:
    fname = 'test0-nt64-uniform.npz'
else:
    fname = 'test0.npz'

data = np.load(fname)
pos = data['pos']
R   = data['Rlag']

#plt.scatter(pos[:,0],pos[:,1],s=10*R,edgecolor='None',facecolor='k')
#plt.show()

nmean = npart / boxsize**3
Rmean = (3.*Nneighbors/4./np.pi/nmean)**(1./3.)

delta = Rmean**3 / R**3 - 1

print 'mean delta = ',delta.mean(),R.min(),R.max(),R.mean(),Rmean,delta.min(),delta.max()

#N, bins = np.histogram(np.log10(1+delta),bins=100)
N, bins = np.histogram(delta,bins=100,range=(-2,2))
#N, bins, patches = plt.hist(delta,bins=100,range=(-2,2))
centers = (bins[:-1] + bins[1:]) / 2
db= bins[1]-bins[0]
dbin = db * N.sum()
N  = N / dbin
print N.min(),N.max()
pmass = 2.775e11*0.266*0.71**2*(200./0.71)**3/npart*32
print 'integral = ',N.sum()*db
plt.plot(centers,N)
plt.show()
