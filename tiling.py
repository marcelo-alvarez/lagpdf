import scipy as sp
import numpy as np
from scipy.spatial import *
import glob
import sys
from readparticles import *
from measurement   import *
from parameters    import * 

def tile2tiles(tile,ntile):
    ix = tile / ntile**2
    iy = (tile - ix * ntile**2) / ntile
    iz = (tile - ix * ntile**2) - iy * ntile
    return ix,iy,iz

def tile2bbox(tile,ntile,buffersize):

    ix,iy,iz = tile2tiles(tile,ntile)

    l1b = buffersize
    l2b = 1-buffersize
    dtile = (l2b-l1b) / ntile

    x1 = l1b + ix*dtile - buffersize
    x2 = x1  + dtile    + 2 * buffersize

    y1 = l1b + iy*dtile - buffersize
    y2 = y1  + dtile    + 2 * buffersize

    z1 = l1b + iz*dtile - buffersize
    z2 = z1  + dtile    + 2 * buffersize

    return x1,x2,y1,y2,z1,z2

def tile2bbox_nobuff(tile,ntile,buffersize):

    ix,iy,iz = tile2tiles(tile,ntile)

    l1b = buffersize
    l2b = 1-buffersize
    dtile = (l2b-l1b) / ntile

    x1 = l1b + ix*dtile 
    x2 = x1  + dtile    

    y1 = l1b + iy*dtile 
    y2 = y1  + dtile    

    z1 = l1b + iz*dtile 
    z2 = z1 + dtile     

    return x1,x2,y1,y2,z1,z2

def shift(l, n):
    return l[n:] + l[:n]

def splitparticles(rank,comm,tile,ntile,buffersize):

    fnames=glob.glob(path+prefix)
    fnames=shift(fnames,rank)

    ix,iy,iz = tile2tiles(tile,ntile)
    x1, x2, y1, y2, z1, z2 = tile2bbox(tile,ntile,buffersize)

    npart=0
    i=0
    x=np.zeros(0)
    y=np.zeros(0)
    z=np.zeros(0)
    for fname in fnames:
        i+=1
        if rank==0: print 'rank',rank,'reading file',i,'of',len(fnames),fname,
        nameonly=fname[len(path):]
        fastname=fastpath+nameonly+'.npz'
        if readfast==False:
            xc,yc,zc,npart2 = getparticles(fname)
            np.savez(fastname,xc=xc,yc=yc,zc=zc)
        else:
            data=np.load(fastname)
            xc=data['xc'];yc=data['yc'];zc=data['zc']
            npart2=len(xc)
                         
        if uniform:
            npart2 = 64**3
            xc=np.random.uniform(size=npart2)        
            yc=np.random.uniform(size=npart2)        
            zc=np.random.uniform(size=npart2)
        
        dm = [(xc>x1) & (xc<x2) &
              (yc>y1) & (yc<y2) &
              (zc>z1) & (zc<z2) ]
        dm = tuple(dm)
        npartc = len(xc[dm])
        if npartc > 0:
            x = np.concatenate((x,xc[dm]))
            y = np.concatenate((y,yc[dm]))
            z = np.concatenate((z,zc[dm]))
        nparttot = len(x)
        if rank == 0:
            outstr='\rnpartc, nparttot = '+str(npartc)+' '+str(nparttot)+' for file '+str(i)+' of '+str(len(fnames))+' on tile '+str(tile)+' of '+str(ntile**3)+'              '
            sys.stdout.write('%s\r' % outstr)
            sys.stdout.flush()
        comm.barrier()
    sys.exit()
    if tile == 0: print ''
    pos = np.concatenate((x,y,z))
    pos = np.reshape(pos,(3,nparttot))
    pos = pos.transpose()

    return pos

def inbbox(pos,bounds):
    
    dm = [(pos[:,0]>bounds[0]) & (pos[:,0]<bounds[1]) &
          (pos[:,1]>bounds[2]) & (pos[:,1]<bounds[3]) &
          (pos[:,2]>bounds[4]) & (pos[:,2]<bounds[5]) ]

    return tuple(dm)

def removebuffer(pos,Rlag,tile,ntile,buffersize):
    bounds = np.asarray((tile2bbox_nobuff(tile,ntile,buffersize)))
    dm = tuple(inbbox(pos,bounds))
    return pos[dm][:],Rlag[dm]

def getpdfsingle(tile,ntile,buffersize):
    pos = splitparticles(tile,ntile,buffersize)
    print 'split done'
    Rlag = ReturnDistanceToNthNeighbor(pos,Nneighbors)
    print 'length of R before buffer remove',len(Rlag)
    pos, Rlag = removebuffer(pos,Rlag,tile,ntile,buffersize)
    print 'length of R after buffer remove',len(Rlag)

    pos  *= boxsize
    Rlag *= boxsize

    np.savez('test.npz',pos=pos,Rlag=Rlag)





