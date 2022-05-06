import stages as sta
import time
import matplotlib.pyplot as plt
import mfli
import numpy as np

lockin=mfli.MFLI()
lockin.set_oscillator(0.0)
mystage=sta.Stage3()
#time.sleep(1)

xvals=np.arange(0.,20.,1.)
yvals=np.arange(10.,30.,1.)
xvals=np.arange(7.5,17.5,.2)
yvals=np.arange(17.5,22.5,.1)
data=np.zeros((xvals.size,yvals.size))
for i in range(xvals.size):
    for j in range(yvals.size):
        print(i)
        print(j)
        mystage.set_pos_mm(xvals[i],yvals[j],0)
        time.sleep(2)
        data[i,j]=lockin.get_R()
plt.pcolor(xvals,yvals,data)
plt.colorbar()
plt.show()

