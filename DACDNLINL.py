
import re
import pylab as plt
import numpy as np
import pandas as pd
#from enthought.mayavi import mlab

vbuf_raw=[]
vubuf_raw=[]
vbuf_aver=[]
vubuf_aver=[]
DNL_ubuf=[]
INL_ubuf=[]
DNL_buf=[]
INL_buf=[]
DNL_buf1=[]
DNL_ubuf1=[]
INL_buf1=[]
INL_ubuf1=[]
code = np.linspace(0, 4096, 4096)

buf_surf=[[0 for col in range(4096)] for row in range(16)]
ubuf_surf=[[0 for col in range(4096)] for row in range(16)]
fin=open("dac_16hit.txt","r")
fdatalog=open("dac_datalog.txt","w")

for line in fin:
    info=line.strip("\n")
    infogroup=re.split("[\t]+",info)
    vbuf_raw.append(float(infogroup[0]))
    vubuf_raw.append(float(infogroup[1]))
vbuf1=[]
vubuf1=[]
#print len(vbuf_raw)    
for i in range(0,len(vbuf_raw)/16):
    #print i
    vb=np.mean(vbuf_raw[i*16:i*16+16])
    vu=np.mean(vubuf_raw[i*16:i*16+16])
    vbuf1.append(vbuf_raw[i*16])
    vubuf1.append(vubuf_raw[i*16])
    vbuf_aver.append(vb)
    vubuf_aver.append(vu)
    for j in range(0,16):
        buf_surf[j][i]=vbuf_raw[i*16+j]
        ubuf_surf[j][i]=vubuf_raw[i*16+j]
print vbuf1[4095]

df_buf=pd.DataFrame(buf_surf)
df_ubuf=pd.DataFrame(ubuf_surf)
mean_buf=df_buf.mean()
mean_ubuf=df_ubuf.mean()
max_buf=df_buf.max()
max_ubuf=df_ubuf.max()
min_buf=df_buf.max()
min_ubuf=df_ubuf.max()
range_buf=df_buf.apply(lambda x: x.max() - x.min())
range_ubuf=df_ubuf.apply(lambda x: x.max() - x.min())
std_buf=df_buf.std()
std_ubuf=df_ubuf.std()
#plt.figure(1)
#df_buf.boxplot()
#plt.figure(2)
#df_ubuf.boxplot()

vLSB=3.0/4096 
vbuf_lf=np.polyfit(code,vbuf_aver,1)    
vubuf_lf=np.polyfit(code,vubuf_aver,1) 
vbuf1_lf=np.polyfit(code,vbuf1,1)    
vubuf1_lf=np.polyfit(code,vubuf1,1) 
offset_buf=vbuf_lf[1]
offset_ubuf=vubuf_lf[1]
offset_buf1=vbuf1_lf[1]
offset_ubuf1=vubuf1_lf[1]
print "The offset error of buffered output is "+str(offset_buf/vLSB)+' LSB.'
print "The offset error of raw output is "+str(offset_ubuf/vLSB)+' LSB.'
print "The gain error of buffered output is "+str((1-vbuf_lf[0]/vLSB)*100)+'%.'
print "The gain error of raw output is "+str((1-vbuf_lf[0]/vLSB)*100)+'%.'
fdatalog.write("The offset error of buffered output is "+str(offset_buf/vLSB)+" LSB.\n")
fdatalog.write("The offset error of raw output is "+str(offset_ubuf/vLSB)+" LSB.\n")
fdatalog.write("The gain error of buffered output is "+str((1-vbuf_lf[0]/vLSB)*100)+"%.\n")
fdatalog.write("The gain error of raw output is "+str((1-vbuf_lf[0]/vLSB)*100)+"%.")

DNL_buf.append(0)
DNL_ubuf.append(0)
DNL_buf1.append(0)
DNL_ubuf1.append(0)    
for i in range(1,len(vbuf_aver)):
    DNL_buf.append((vbuf_aver[i]-vbuf_aver[i-1])/vLSB-1)
    DNL_ubuf.append((vubuf_aver[i]-vubuf_aver[i-1])/vLSB-1)
    DNL_buf1.append((vbuf1[i]-vbuf1[i-1])/vLSB-1)
    DNL_ubuf1.append((vubuf1[i]-vubuf1[i-1])/vLSB-1)
    
for i in range(0,len(vbuf_aver)):
    INL_buf.append((vbuf_aver[i]-(i*vbuf_lf[0]+vbuf_lf[1]))/vLSB)
    INL_ubuf.append((vubuf_aver[i]-(i*vubuf_lf[0]+vubuf_lf[1]))/vLSB)
    INL_buf1.append((vbuf1[i]-(i*vbuf1_lf[0]+vbuf1_lf[1]))/vLSB)
    INL_ubuf1.append((vubuf1[i]-(i*vubuf1_lf[0]+vubuf1_lf[1]))/vLSB)        

#for i in range(0,len(vbuf_raw)/16):
#    for j in range(0,16):
#        buf_surf[i][j]=vbuf_raw[i*16+j]-(i*vbuf_lf[0]+vbuf_lf[1])
#        ubuf_surf[i][j]=vubuf_raw[i*16+j]-(i*vubuf_lf[0]+vubuf_lf[1])
#        
#x, y = np.ogrid[0:4096:4096j, 0:16:16j]
#pl1 = mlab.surf(x, y, buf_surf , warp_scale="auto")
#mlab.axes(xlabel='x', ylabel='y', zlabel='z')
#mlab.outline(pl1)       
plt.figure(1)
plt.subplot(2,4,1)
plt.plot(code,mean_buf,label="mean_buf",color="blue",linewidth=1) 
plt.title("Mean value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,2)
plt.plot(code,mean_ubuf,label="mean_ubuf",color="blue",linewidth=1) 
plt.title("Mean value unbuffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,3)
plt.plot(code,max_buf,label="max_buf",color="blue",linewidth=1) 
plt.title("Max value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,4)
plt.plot(code,max_ubuf,label="max_ubuf",color="blue",linewidth=1) 
plt.title("Max value unbuffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,5)
plt.plot(code,min_buf,label="min_buf",color="blue",linewidth=1) 
plt.title("Min value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,6)
plt.plot(code,min_ubuf,label="min_ubuf",color="blue",linewidth=1) 
plt.title("Min value unbuffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,7)
plt.plot(code,range_buf,label="range_buf",color="blue",linewidth=1) 
plt.title("Range value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,8)
plt.plot(code,range_ubuf,label="range_ubuf",color="blue",linewidth=1) 
plt.title("Range value unbuffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.figure(2)
plt.subplot(2,2,1)
plt.plot(code,DNL_buf,label="DNL_buf",color="blue",linewidth=1) 
plt.title("DNL_buf plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()  
  
plt.subplot(2,2,2)
plt.plot(code,DNL_ubuf,label="DNL_ubuf",color="blue",linewidth=1) 
plt.title("DNL_ubuf plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()    

plt.subplot(2,2,3)
plt.plot(code,INL_buf,label="INL_buf",color="red",linewidth=1)
plt.title("INL_ubuf plot vs. code") 
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()    

plt.subplot(2,2,4)        
plt.plot(code,INL_ubuf,label="INL_ubuf",color="red",linewidth=1) 
plt.title("INL_ubuf plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()

plt.figure(3)
plt.subplot(2,2,1)
plt.plot(code,DNL_buf1,label="DNL_buf1",color="blue",linewidth=1) 
plt.title("DNL_buf hit1 plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()  
  
plt.subplot(2,2,2)
plt.plot(code,DNL_ubuf1,label="DNL_ubuf1",color="blue",linewidth=1) 
plt.title("DNL_ubuf hit1 plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()    

plt.subplot(2,2,3)
plt.plot(code,INL_buf1,label="INL_buf1",color="red",linewidth=1)
plt.title("INL_ubuf hit1 plot vs. code") 
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend()    

plt.subplot(2,2,4)        
plt.plot(code,INL_ubuf1,label="INL_ubuf1",color="red",linewidth=1) 
plt.title("INL_ubuf hit1 plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("LSB")
plt.legend() 

plt.figure(4)   
plt.subplot(2,4,1)
plt.hist(df_buf[0:16][2047], 16, color="green") 
plt.title("Distribution of unbuf code: 2047")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")

plt.subplot(2,4,2)
plt.hist(df_buf[0:16][172], 16) 
plt.title("Distribution of unbuf anomalous code: 172")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")

plt.subplot(2,4,3)
plt.hist(df_buf[0:16][176], 16) 
plt.title("Distribution of unbuf anomalous code: 176")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")

plt.subplot(2,4,4)
plt.hist(df_buf[0:16][228], 16) 
plt.title("Distribution of unbuf anomalous code: 228")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")

plt.subplot(2,4,5)
plt.hist(df_buf[0:16][1180], 16) 
plt.title("Distribution of unbuf anomalous code: 1180")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")

plt.subplot(2,4,6)
plt.hist(df_buf[0:16][1320], 16) 
plt.title("Distribution of unbuf anomalous code: 1320")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("Count")


plt.subplot(2,4,7)
plt.plot(code,range_buf,label="range_buf",color="blue",linewidth=1) 
plt.title("Range value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(2,4,8)
plt.plot(code,range_ubuf,label="range_ubuf",color="blue",linewidth=1) 
plt.title("Range value unbuffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.figure(5)
plt.subplot(3,1,1)
plt.plot(code,range_buf,label="range_buf",color="blue",linewidth=1) 
plt.title("Range value buffer plot vs. code")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(3,1,2)
plt.plot(code[4000:4096:1],range_buf[4000:4096:1],label="range_buf",color="blue",linewidth=1) 
plt.title("Range value buffer plot vs. code (Zoomed in)")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")

plt.subplot(3,1,3)
plt.plot(code[0:100:1],range_buf[0:100:1],label="range_buf",color="blue",linewidth=1) 
plt.title("Range value buffer plot vs. code (Zoomed in)")
plt.grid(True)
plt.xlabel("code") 
plt.ylabel("V")
  
plt.show()
    
