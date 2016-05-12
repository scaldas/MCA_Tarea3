import numpy as np
import matplotlib.pyplot as plt
import glob
import sys                

if(len(sys.argv) != 2):
    sys.exit("energy.py i_snap")
    
files = glob.glob("output*.dat")
n_files = len(files)
def energy(data):
    E = data[:,6].sum() + data[:,7].sum()    
    return E

def radius(data):
    E_pot = data[:,6]
    min_pot = np.argmin(E_pot)
    x = data[:,0] - data[min_pot, 0]
    y = data[:,1] - data[min_pot, 1]
    z = data[:,2] - data[min_pot, 2]
    r = np.sqrt(x**2 + y**2 +z**2)
    r = np.sort(r)
    return r[1:]

E = []
i_snap = int(sys.argv[1])
for i in range(i_snap):
    data_init = np.loadtxt("output_{}.dat".format(i))
    E_final = energy(data_init)
    E.append(E_final)


plt.figure()
plt.plot(E)
plt.ylabel('E')
plt.xlabel('numero de iteraciones')
#plt.show()
plt.savefig('energy.png')
