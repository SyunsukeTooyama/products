import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import itertools
L=10
h=1
m=1
grid=100
number=10
t=60

xs=np.linspace(0,L,grid)
fig,ax=plt.subplots()
#ax.set_axis_off()
ax.axvspan(-1, 0, color="gray")
ax.axvspan(10, 11, color="gray")
ax.set_xlim(-1,11)
ax.axes.yaxis.set_visible(False)

for p in ['left','top','right']:
  ax.spines[p].set_visible(False)
f=[]
for n in range(number):
    energy=n**2*h**2/(8*m*L)
    psi_time=np.exp(-1*1j*energy*0)
    psi_posi=np.sin(n*np.pi*xs/L)
    line,=ax.plot(xs,psi_posi*psi_time+2*n)
    f.append(line)  


def wave_func(time):
    for n in range(number):
        energy=n**2*h**2/(8*m*L)
        psi_time=np.exp(-1*1j*energy*time)
        psi_posi=np.sin(n*np.pi*xs/L)
        f[n].set_ydata(psi_posi*psi_time+2*n)        
    return f


ani=animation.FuncAnimation(fig,wave_func,interval=10,save_count=100)

plt.show()
ani.save(filename=r"C:\Users\syuns\python\1.gif", writer="pillow")