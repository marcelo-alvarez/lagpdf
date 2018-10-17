import scipy as sp
import numpy as np
from scipy.spatial import *
import glob
import sys

path='./output_00010/'

def readfortranfourbyte(file):
    bytesinblock = np.fromfile(file,count=1,dtype=np.int32)[0]
    return bytesinblock

def getparticles(fname):
    file = open(fname)

    # read first part of header
    bytesinblock = readfortranfourbyte(file)
    ncpu2  = np.fromfile(file,count=1,dtype=np.int32)[0]
    bytesinblock = readfortranfourbyte(file)

    bytesinblock = readfortranfourbyte(file)
    ndim2  = np.fromfile(file,count=1,dtype=np.int32)[0]
    bytesinblock = readfortranfourbyte(file)

    bytesinblock = readfortranfourbyte(file)
    npart2 = np.fromfile(file,count=1,dtype=np.int32)[0]
    readfortranfourbyte(file)

    # read rest of header
    for i in np.arange(5):
        nbytes1=readfortranfourbyte(file)
        dum=np.fromfile(file,count=nbytes1/4,dtype=np.int32)[0]
        nbytes2=readfortranfourbyte(file)

    # read particle positions
    nbytes1=readfortranfourbyte(file)
    npartfromheader = nbytes1 / 8
    if npartfromheader != npart2:
        print 'error', npartfromheader,npart2
        sys.exit()

    x = np.fromfile(file,count=npart2,dtype=np.float64)
    nbytes1=readfortranfourbyte(file)

    nbytes1=readfortranfourbyte(file)
    y = np.fromfile(file,count=npart2,dtype=np.float64)
    nbytes1=readfortranfourbyte(file)

    nbytes1=readfortranfourbyte(file)
    z = np.fromfile(file,count=npart2,dtype=np.float64)
    nbytes1=readfortranfourbyte(file)

    return x,y,z,npart2







