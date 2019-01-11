import scipy as sp
import numpy as np
from scipy.spatial import *
import glob
import sys
from readparticles import *
from measurement   import *
from parameters    import *

import mpi4py.rc
if serial: mpi4py.rc.initialize = False
from mpi4py import MPI

if MPI.Is_initialized():
    comm     = MPI.COMM_WORLD
    rank     = comm.Get_rank()
    nproc    = comm.Get_size()
    parallel = True
else:
    nproc = ntile**3
    comm     = 0
    parallel = False

if serial:
    rank=0
    tile=0
    getrlagsingle(rank,comm,tile,ntile,buffersize)
    sys.exit(0)

numtiles = ntile**3
Rlag=np.zeros(0)
if rank == 0: print nproc,ntile
for tile in np.arange(numtiles):
    if tile % nproc ==  rank:
        Rlagc=getrlagsingle(rank,comm,tile,ntile,buffersize)
        Rlag = np.concatenate((Rlagc,Rlag))

comm.barrier()

Rlag = Rlag.astype(np.float32)

npart  = np.asarray([len(Rlag)],dtype=np.int32)

npartt = np.asarray([0],dtype=np.int32)
comm.Allreduce(npart,npartt)

nparteach=np.zeros(nproc,np.int32)
comm.Allgather(npart,nparteach)

offsets=np.roll(np.cumsum(nparteach),1); offsets[0]=0
nparteach=tuple(nparteach); offsets=tuple(offsets)

Rlagt=None
if rank==0: Rlagt=np.empty(npartt[0],dtype=np.float32)

sendbuf=[Rlag, nparteach[rank],MPI.FLOAT]
recvbuf=[Rlagt,nparteach,offsets,MPI.FLOAT]
comm.Gatherv(sendbuf,recvbuf,root=0)

if rank==0:
    print 'local and total sizes of Rlag on root:',len(Rlag),len(Rlagt)
    np.savez(pdffname,Rlagt=Rlag)




