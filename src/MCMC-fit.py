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
    #print("min_pot", min_pot)
    x = data[:,0] - data[min_pot, 0]
    y = data[:,1] - data[min_pot, 1]
    z = data[:,2] - data[min_pot, 2]
    r = np.sqrt(x**2 + y**2 +z**2)
    r = np.sort(r)
    return r[1:]

data_init = np.loadtxt("output_inicial.dat")
E_init = energy(data_init)
r_init = radius(data_init)
print("La energia inicial fue {}").format(E_init)

data_final = np.loadtxt("output_final.dat")
E_final = energy(data_final)
r_final = radius(data_final)
r_final = np.sort(r_final)
log_r_final = np.log10(r_final)

h, c = np.histogram(log_r_final)
print("La energia final fue {}").format(E_final)

print("Se tiene un {0:.2f}% de la energia inicial\n").format(100*E_final/E_init)

log_r_center = 0.5 * (c[1:]+c[:-1])


#Importacion de datos
log10r = log_r_center
log10densidad = np.log10(h)-2.0*log_r_center

r = np.power(10, log10r)
densidad = np.power(10,log10densidad)

#Definicion de funcion que calcula el likelihood

def likelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*np.sum((y_obs-y_model)**2)
	return -chi_squared

#Definicion de la funcion del modelo

def model(r, log_rho0, alpha, beta, rc):
	return log_rho0 + alpha*(np.log10(rc/r)) - beta*np.log10(1+r/rc)

#Inicializacion de caminata
log_rho0_walk = np.empty((0))
alpha_walk = np.empty((0))
beta_walk = np.empty((0))
log_rc_walk = np.empty((0))
l_walk = np.empty((0))

'''
El ajuste hecho depende mucho de los parametros iniciales. Un cambio en uno de los parametros iniciales
crea una marcha que resulta en valores de parametros muy diferentes. Se usan los parametros iniciales que
lograron un mejor ajuste pero dado su valor de likelihood hacen que se mantengan constantes durante toda la marcha.
'''
log_rho0_walk = np.append(log_rho0_walk, 4)
alpha_walk = np.append(alpha_walk, 1)
beta_walk = np.append(beta_walk, 1)
log_rc_walk = np.append(log_rc_walk, -1)
	
y_init = model(r, log_rho0_walk[0], alpha_walk[0], beta_walk[0], np.power(10, log_rc_walk[0]))
l_walk = np.append(l_walk, likelihood(densidad, y_init))


#Caminata sobre valores de parametros
n_iterations = 50000

for i in range(n_iterations):
    log_rho0_prime = np.random.normal(log_rho0_walk[i], 0.1) 
    alpha_prime = np.random.normal(alpha_walk[i], 0.1)
    beta_prime = np.random.normal(beta_walk[i], 0.1)
    log_rc_prime = np.random.normal(log_rc_walk[i], 0.1)

    rc_init = np.power(10, log_rc_walk[i])
    rc_prime = np.power(10, log_rc_prime)
   	
    y_init = model(r, log_rho0_walk[i], alpha_walk[i], beta_walk[i], rc_init)
    y_prime = model(r, log_rc_prime, alpha_prime, beta_prime, rc_prime)
	    
    l_prime = likelihood(log10densidad, y_prime)
    l_init = likelihood(log10densidad, y_init)
	    
    alpha = l_prime/l_init
    if(alpha<=1.0):
        log_rho0_walk = np.append(log_rho0_walk, log_rho0_prime)
        alpha_walk = np.append(alpha_walk, alpha_prime)
        beta_walk = np.append(beta_walk, beta_prime)
        log_rc_walk = np.append(log_rc_walk, log_rc_prime)
        l_walk = np.append(l_walk, l_prime)
    else:
        beta = np.random.random()
        if(np.log(beta)<= -alpha):
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

#Calculo de incertidumbres
'''
El calculo de incertidumbres se hace teniendo en cuenta el percentil 16 para el limite
inferior y 84 para el limite superior. Se comparan estos valores con el valor obtenido
para encontrar las incertidumbres superiores e inferiores.

Las incertidumbres se imprimen con el formato
Valor obtenido -incertidumbre inferior +incertidumbre superior
'''
alpha_percentile16 = np.percentile(alpha_walk, 16)
beta_percentile16 = np.percentile(beta_walk, 16)
rho0_percentile16 = np.power(10, np.percentile(log_rho0_walk, 16))
rc_percentile16 = np.power(10, np.percentile(log_rc_walk, 16))

alpha_percentile84 = np.percentile(alpha_walk, 84)
beta_percentile84 = np.percentile(beta_walk, 84)
rho0_percentile84 = np.power(10, np.percentile(log_rho0_walk, 84))
rc_percentile84 = np.power(10, np.percentile(log_rc_walk, 84))


buncertainty_alpha = best_alpha - alpha_percentile16
if(buncertainty_alpha < 0): buncertainty_alpha = 0

buncertainty_beta = best_beta - beta_percentile16
if(buncertainty_beta < 0): buncertainty_beta = 0

buncertainty_rc = best_rc - rc_percentile16
if(buncertainty_rc < 0): buncertainty_rc = 0

buncertainty_rho0 = best_rho0 - rho0_percentile16
if(buncertainty_rho0 < 0): buncertainty_rho0 = 0

uuncertainty_alpha = alpha_percentile84 - best_alpha
if(uuncertainty_alpha < 0): uuncertainty_alpha = 0

uuncertainty_beta = beta_percentile84 - best_beta
if(uuncertainty_beta < 0): uuncertainty_beta = 0

uuncertainty_rc = rc_percentile84 - best_rc
if(uuncertainty_rc < 0): uuncertainty_rc = 0

uuncertainty_rho0 = rho0_percentile84 - best_rho0
if(uuncertainty_rho0 < 0): uuncertainty_rho0 = 0

#Print resultados valores de parametros
print("Mejores valores de parametros")
print("Rho0: {0} -{1} +{2}").format(best_rho0, buncertainty_rho0, uuncertainty_rho0)
print("Alpha: {0} -{1} +{2}").format(best_alpha, buncertainty_alpha, uuncertainty_alpha)
print("Beta: {0} -{1} +{2}").format(best_beta, buncertainty_beta, uuncertainty_beta)
print("Rc: {0} -{1} +{2}").format(best_rc, buncertainty_rc, uuncertainty_rc)

#Calculo de densidad con mejores parametros
log_densidadexp = model(r, log_rho0_walk[max_index], best_alpha, best_beta, best_rc)

#Grafica resultados simulacion y MCMC fit
plt.figure()
plt.plot(log10r, log10densidad, label = "Simulation", c  = "red")
plt.plot(log10r, log_densidadexp, label = "MCMC")
plt.legend()
plt.ylabel(r'$log(\rho)$', fontsize = 18)
plt.xlabel(r'$log(r)$', fontsize = 18)
plt.title('Perfil de densidad')
plt.savefig("perfil_densidad.png")

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

plt.savefig("caminatas.png")			
