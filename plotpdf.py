import numpy as np
import matplotlib.pyplot as plt
from parameters import *
import csv

rank = 0
npart = 1024.**3
grid_spacing = boxsize / 1024.

fname=pdffname
fname='test_200_3000_8.0.npz'
print 'fname is ',fname
data = np.load(fname)
pos = data['pos']
R   = data['Rlag']

#plt.scatter(pos[:,0],pos[:,1],s=10*R,edgecolor='None',facecolor='k')
#plt.show()

nmean = npart / boxsize**3
Rmean = (3.*Nneighbors/4./np.pi/nmean)**(1./3.)

delta = Rmean**3 / R**3 - 1

delta.tofile('delta.bin')
print ('mean delta, rms, max R = ',delta.mean(), delta.var()**0.5,R.max(),
       R.max()/grid_spacing)

Ntot = len(delta)*1.0
print 'Ntot = ',Ntot
nbins=500
delta_min=-0.95
delta_max=1e5
lnopdelta = np.log(1+delta)
lnopdelta_min=np.log(1+delta_min)
lnopdelta_max=np.log(1+delta_max)
#N, bins = np.histogram(delta,bins=nbins,range=(delta_min,delta_max))
N, bins = np.histogram(lnopdelta,bins=nbins,range=(lnopdelta_min,lnopdelta_max))
db= bins[1]-bins[0]
N = N / Ntot
lnopdelta_bin = (bins[:-1] + bins[1:]) / 2
opdelta_bin = np.exp(lnopdelta_bin)
delta_bin = opdelta_bin - 1
#N  = N / db
N  = N / db / opdelta_bin
print N.min(),N.max()
pmass = 2.775e11*0.266*0.71**2*(200./0.71)**3/npart*32
print 'integral, rms = ',((N*opdelta_bin).sum()*db,
                          (N*delta_bin*opdelta_bin).sum()*db,
                          (N*delta_bin**2*opdelta_bin).sum()*db)
plt.loglog(opdelta_bin,N,label=r'buffer = 8 Mpc')
plt.gca().set_xlim((1e-2,1e2))
plt.gca().set_ylim((1e-3,2))
plt.legend()
def plotanalytic(fname):
    file = open(fname,'rb')
    data = csv.reader(file,delimiter=',')
    table = [row for row in data]
    delta=np.zeros(500)
    p=np.zeros(500)
    for i in np.arange(500):
        delta[i]=table[i][0]
        p[i]=table[i][1]
    plt.loglog(delta,p)

#plotanalytic('data-forMarcelo_sigma_2.0.csv')
#plotanalytic('data-forMarcelo_sigma_2.5.csv')
plotanalytic('data-forMarcelo_3000neighbors.csv')

#plt.show()

