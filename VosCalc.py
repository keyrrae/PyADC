
#import string
#import os 
import pylab as plt
import numpy as np
lotname="VTN" 
vcclist = ["2.2","2.4","3.0","3.6"]
pwrmdlist = ["HP","LP"]
colorlist1 = ["blue","green","red","cyan"]
colorlist2 = ["magenta","black","orange","chartreuse"]
ipw = 0

for pw in pwrmdlist:
    
    index = 0
    for vcc in vcclist:
        vos = []
        vin = np.linspace(0, float(vcc), 4096)
        funbuf = open(lotname+"_310_"+vcc+"_0_"+str(ipw)+"_Int_Unbuf.txt","r")  
        fbuf = open(lotname+"_310_"+vcc+"_0_"+str(ipw)+"_Int_Buf.txt","r")  
        vunbuf = funbuf.readlines()
        vbuf = fbuf.readlines()
        #print vbuf[1]
        vos.append(float(vbuf[1])-float(vunbuf[1].strip('\n')))
        vbuf[0] = vbuf[1]
        vbuf[4095] = vbuf[4094]
        for i in range(1,4095):
            vo_unbuf = float(vunbuf[i].strip('\n'))
            vo_buf = float(vbuf[i].strip('\n'))
            vos.append(vo_buf - vo_unbuf)
        vos.append(float(vbuf[4094].strip('\n'))-float(vunbuf[4094].strip('\n')))    
        #print len(vos)
        #print len(vin)
        plt.subplot(2,2,index+1)
        
        #plt.figure(index)
        if pw == "HP" :
            plt.plot(vin,vos,label=pw,color=colorlist1[index],linewidth=1) 
        else:
            plt.plot(vin,vos,label=pw,color=colorlist2[index],linewidth=0.4)             
        plt.xlabel("Vin(V)") 
        plt.ylabel("Vos(V)")
        #plt.title("Vos plot vs. Vin(0 to DVCC)")
        plt.title("Lot="+lotname+", Vos plot vs. Vin(0 to DVCC), DVCC="+vcclist[index])
        # PowerMode=+pw)
        plt.grid(True)
        #plt.ylim(-0.002,0.002)
        plt.legend()
        

        
        index = index + 1
    ipw = ipw + 1

plt.show()             
#    
