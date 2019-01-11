path='./output_00010/'
fastpath='/data34/codis/LagSC/output_npz/'
prefix='part*'
Nneighbors=3000
boxsize = 200 # Mpc/h
buffersize_Mpc = 4.5
buffersize = buffersize_Mpc / boxsize

serial   = False
uniform  = False
debug    = False
readfast = True

ntile = 8
pdffname='test'+'_'+str(boxsize)+'_'+str(Nneighbors)+'_'+str(buffersize_Mpc)+'.npz'
