import numpy as np
import matplotlib.pyplot as plt
import sys               
import subprocess

if(len(sys.argv) != 2):
    sys.exit("energy.py i_snap")

def energy(data):
    E = data[:,6].sum() + data[:,7].sum()    
    return E

E = []
x = []
i_snap = int(sys.argv[1])

for i in range(100):
	p = subprocess.Popen(['./a.out', '1000', '0.1', '%s' % (i*10)], bufsize=2048, stdin=subprocess.PIPE)
	p.wait()
	data_init = np.loadtxt("./output_{}.dat".format(i_snap))
	E_final = energy(data_init)
	E.append(E_final)
	x.append(i*10)
plt.figure()
plt.plot(x, E)
plt.ylabel('E_final')
plt.xlabel('numero de buckets')
plt.savefig('buckets.png')
