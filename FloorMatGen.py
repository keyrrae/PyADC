import re
#import pylab as plt
import numpy as np
import random
#import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

class Cunit:
    def __init__(self,row,col,cinit,name):
        self.cgrad=col*xlen*xdir*xgrad/1e-6+row*ylen*ydir*ygrad/1e-6
        self.cval=cinit*random.gauss(1,sigma)+self.cgrad
        self.name=name
    
class Csum:
    cval=0.0
    def __init__(self,name):
        self.name=name

EnGrad=1
EnRand=1
xlen=5e-6
ylen=10e-6    
xdir=1
ydir=1
cinit=100e-15       
        
for fpnum in range(6):
    cmatrix=[]
    cRow=[]
    cunits=[]

    fcin=open("CapFloorPlan"+str(fpnum)+".csv","r")
    for line in fcin:
        info = line.strip(',')
        info=re.split("[,\n]",line)
        cRow=[]
        for i in range(len(info)-1):
            cRow.append(info[i])
            cunits.append(info[i])
        cmatrix.append(cRow)    
    fcin.close()

    cnames=sorted(list(set(cunits)))
    csumlist=[]
    for i in range(len(cnames)):
        csumlist.append(Csum(cnames[i]))    
        
    rnum=len(cmatrix)
    cnum=len(cmatrix[0])

    xgrad=EnGrad*0.001*cinit/(cnum*xlen*1e6) 
    #xgrad=EnGrad*5e-18 # cap gradient F/um
    ygrad=EnGrad*0.001*cinit/(cnum*xlen*1e6) 
    #ygrad=EnGrad*5e-18 # cap gradient F/

    sigma=EnRand*0.001    

    caplist= [[Cunit(row,col,cinit,cmatrix[row][col]) for col in range(cnum)] for row in range(rnum)]

    cmin=1
    cmax=0
    cvallist=[]
    for i in range(rnum):
        cvalcol=[]
        for j in range(cnum):
            cvalcol.append(caplist[i][j].cval)
            if caplist[i][j].cval >= cmax:
                cmax=caplist[i][j].cval
            if caplist[i][j].cval <= cmin:
                cmin=caplist[i][j].cval
            for k in range(len(csumlist)):
                if caplist[i][j].name == csumlist[k].name:
                    csumlist[k].cval = csumlist[k].cval + caplist[i][j].cval
        cvallist.append(cvalcol)
                            
    fig = plt.figure(fpnum)
    ax = fig.gca(projection='3d')
    X, Y = np.mgrid[0:rnum*xlen:rnum*1j,0:ylen*cnum:cnum*1j]
    Z = cvallist
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)

    ax.set_xlabel('X')
    ax.set_xlim(0, rnum*xlen)
    ax.set_ylabel('Y')
    ax.set_ylim(0, ylen*cnum)
    ax.set_zlabel('Z')
    ax.set_zlim(cmin,cmax)


    fcapsum=open("CapSum"+str(fpnum)+".csv","w")
    for i in range(len(csumlist)):
        fcapsum.write(csumlist[i].name+','+str(csumlist[i].cval)+'\n')
    fcapsum.close()

    fcaparray=open("CapArray"+str(fpnum)+".csv","w")
    for i in range(rnum):
        for j in range(cnum-1):
            fcaparray.write(str(cvallist[i][j])+',')
        fcaparray.write(str(cvallist[i][cnum-1])+'\n')
    fcaparray.close()        

plt.show()
