import numpy as np
import matplotlib.pyplot as plt
import math
import glob
import sys

files = glob.glob("output*.dat")
n_files = len(files)
def energy(data):
    E = data[:,6].sum() + data[:,7].sum()    
    return E

def radius(data):
    E_pot = data[:,6]
    min_pot = np.argmin(E_pot)
    print("min_pot", min_pot)
    x = data[:,0] - data[min_pot, 0]
    y = data[:,1] - data[min_pot, 1]
    z = data[:,2] - data[min_pot, 2]
    r = np.sqrt(x**2 + y**2 +z**2)
    r = np.sort(r)
    return r[1:]

i_snap = 0
data_init = np.loadtxt("output_{}.dat".format(i_snap))
E_init = energy(data_init)
r_init = radius(data_init)
print(E_init)

i_snap = sys.argv[1]
data_init = np.loadtxt("output_{}.dat".format(i_snap))
E_final = energy(data_init)
r_final = radius(data_init)
r_final = np.sort(r_final)
log_r_final = np.log10(r_final)

h, c = np.histogram(log_r_final)
print(E_final)

log_r_center = 0.5 * (c[1:]+c[:-1])


#Importacion de datos
data = np.loadtxt("plotdata.dat", delimiter = ", \t")
log10r = log_r_center
log10densidad = np.log10(h)-2.0*log_r_center

r = np.power(10, log10r)
densidad = np.power(10,log10densidad)

#Definicion de funcion que calcula el likelihood

def likelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*sum((y_obs-y_model)**2)
	return -chi_squared

#Definicion de la funcion del modelo

def model(r, rho0, alpha, beta, rc):
	return rho0/((np.power((r/rc), alpha))*(np.power((1+r/rc),beta)))

#Inicializacion de caminata
log_rho0_walk = np.empty((0))
alpha_walk = np.empty((0))
beta_walk = np.empty((0))
log_rc_walk = np.empty((0))
l_walk = np.empty((0))

log_rho0_walk = np.append(log_rho0_walk, np.random.normal())
alpha_walk = np.append(alpha_walk, np.random.normal())
beta_walk = np.append(beta_walk, np.random.normal())
log_rc_walk = np.append(log_rc_walk, np.random.normal())
	
y_init = model(r, np.power(10, log_rho0_walk[0]), alpha_walk[0], beta_walk[0], np.power(10, log_rc_walk[0]))
l_walk = np.append(l_walk, likelihood(densidad, y_init))


#Caminata sobre valores de parametros
n_iterations = 20000

for i in range(n_iterations):
    log_rho0_prime = np.random.normal(log_rho0_walk[i], 1) 
    alpha_prime = np.random.normal(alpha_walk[i], 1)
    beta_prime = np.random.normal(beta_walk[i], 1)
    log_rc_prime = np.random.normal(log_rc_walk[i], 1)

    rho0_init = np.power(10, log_rho0_walk[i])
    rc_init = np.power(10, log_rc_walk[i])

    rho0_prime = np.power(10, log_rho0_prime)
    rc_prime = np.power(10, log_rc_prime)
   	
    y_init = model(r, rho0_init, alpha_walk[i], beta_walk[i], rc_init)
    y_prime = model(r, rho0_prime, alpha_prime, beta_prime, rc_prime)
	    
    l_prime = likelihood(densidad, y_prime)
    l_init = likelihood(densidad, y_init)
	    
    alpha = l_prime-l_init
    if(alpha>=1.0):
        log_rho0_walk = np.append(log_rho0_walk, log_rho0_prime)
        alpha_walk = np.append(alpha_walk, alpha_prime)
        beta_walk = np.append(beta_walk, beta_prime)
        log_rc_walk = np.append(log_rc_walk, log_rc_prime)
        l_walk = np.append(l_walk, l_prime)
    else:
        beta = np.random.random()
        if(beta<=alpha):
            log_rho0_walk = np.append(log_rho0_walk, log_rho0_prime)
            alpha_walk = np.append(alpha_walk, alpha_prime)
            beta_walk = np.append(beta_walk, beta_prime)
            log_rc_walk = np.append(log_rc_walk, log_rc_prime)
            l_walk = np.append(l_walk, l_prime)
        else:
            log_rho0_walk = np.append(log_rho0_walk, log_rho0_walk[i])
            alpha_walk = np.append(alpha_walk,alpha_walk[i])
            beta_walk = np.append(beta_walk, beta_walk[i])
            log_rc_walk = np.append(log_rc_walk, log_rc_walk[i])
            l_walk = np.append(l_walk, l_init)

#Encontrar mejores valores
max_index = np.argmax(l_walk)
likelihood_obs = l_walk[max_index]
best_rho0 = np.power(10, log_rho0_walk[max_index])
best_alpha = alpha_walk[max_index]
best_beta = beta_walk[max_index]
best_rc = np.power(10, log_rc_walk[max_index])

print(max_index)
print(likelihood_obs)
print(best_rho0)
print(best_alpha)
print(best_beta)
print(best_rc)

#Calculo de densidad con mejores parametros
densidadexp = model(r, best_rho0, best_alpha, best_beta, best_rc)

#Grafica resultados simulacion y MCMC fit
plt.figure()
plt.scatter(log10r, log10densidad, label = "Simulation", c  = "red")
plt.scatter(log10r, np.log10(densidadexp), label = "MCMC")
plt.legend()
plt.ylabel(r'$log(\rho)$')
plt.xlabel(r'$log(r)$')
plt.title('Densidad respecto al radio')
plt.show()

#Grafica caminata de parametros
ax = plt.subplot(2, 1, 1)
plt.plot(alpha_walk, label = r'$\alpha$')
plt.plot(beta_walk, label = r'$\beta$')
plt.plot(log_rc_walk, label = r'$log(r_{c})$')           
plt.legend(loc="best", shadow=True, fancybox=True)
plt.title("Caminatas Parametros")
ax.get_legend().get_title().set_color("red")

ax = plt.subplot(2, 1, 2)
plt.plot(log_rho0_walk, label = r'$log(\rho_{0})$')
plt.legend(shadow=True, fancybox=True, loc = 'best')

ax.set_xlabel('Numero iteracion')
ax.set_ylabel('Valor parametro')

plt.show()			
