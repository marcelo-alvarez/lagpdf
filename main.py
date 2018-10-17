import scipy as sp
import numpy as np
from scipy.spatial import *
import glob
import sys
from readparticles import *
import mpi4py

path='./output_00010/'
ntile=8
nproc = ntile**3
buffersize=0.1

def rank2tiles(rank,ntile):
    ix = rank / ntile**2
    iy = (rank - ix * ntile**2) / ntile
    iz = (rank - ix * ntile**2) - iy * ntile
    return ix,iy,iz

def tiles2bbox(ix,iy,iz,ntile,buffersize):

    l1b = buffersize
    l2b = 1-buffersize
    dtile = (l2b-l1b) / ntile

    x1 = l1b + ix*dtile - buffersize
    x2 = x1  + dtile    + 2 * buffersize

    y1 = l1b + iy*dtile - buffersize
    y2 = y1  + dtile    + 2 * buffersize

    z1 = l1b + iz*dtile - buffersize
    z2 = z1 + dtile     + 2 * buffersize

    return x1,x2,y1,y2,z1,z2

def splitparticles(rank,ntile,buffersize):

    ix,iy,iz = rank2tiles(rank,ntile)
    x1, x2, y1, y2, z1, z2 = tiles2bbox(ix,iy,iz,ntile,buffersize)

    print 'tiling for rank ',rank,':'
    print '    ',x1,x2,y1,y2,z1,z2

    npart=0
    i=0
    x=np.zeros(0)
    y=np.zeros(0)
    z=np.zeros(0)
    for fname in fnames:
        i+=1
        xc,yc,zc,npart2 = getparticles(fname)
        
        dm = [(xc>x1) & (xc<x2) &
              (yc>y1) & (yc<y2) &
              (zc>z1) & (zc<z2) ]
        x = np.concatenate((x,xc[dm]))
        y = np.concatenate((y,yc[dm]))
        z = np.concatenate((z,zc[dm]))
        npartc = len(xc[dm])
        nparttot = len(x)
        print 'npartc, nparttot = ',npartc,nparttot,'for ',i,' of ',len(fnames)

    return x,y,z

# faux parallelization by looping over ranks in serial

fnames=glob.glob(path+'part*')
for rank in np.arange(1):
    x,y,z = splitparticles(rank,ntile,buffersize)
    print 'total npart ',len(x)
    print 'bounds: ',x.min(),x.max(),y.min(),y.max(),z.min(),z.max()






