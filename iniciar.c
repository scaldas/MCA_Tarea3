#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define M_PI 3.14159265358979323846

/*
recibe_input asigna los valores ingresados por parametro a las variables 
correspondientes en el codigo.
 */

void recibe_input(int argc, char **argv, int *n_bodies, double *epsilon){

  if(argc!=3){
    fprintf(stderr, "USAGE: ./nbody N_particles epsilon\n");
    exit(1);
  }
  *n_bodies = atoi(argv[1]);
  *epsilon = atof(argv[2]);

}

/*
init_positions recibe como argumentos punteros para las tres coordenadas de las posiciones
con memoria ya asignada para cada uno.

La funcion llena los vectores que se ingresaron como argumento llenos de posiciones 
para un numero n_bodies que tendran como distancia media entre ellos aproximadamente 1.
 */

void init_positions(double *x, double *y, double *z, double n_bodies){

  double phi, r, theta;
  double R;
  int j;

  R = pow(n_bodies, 1.0/3.0);


  for(j=0; j<n_bodies; j++){

    phi = drand48()*2*M_PI;
    theta = acos(2*drand48()-1);
    r = R*pow(drand48(), 1.0/3.0);

    x[j] = r*sin(theta)*cos(phi);
    y[j] = r*sin(theta)*sin(phi);
    z[j] = r*cos(theta);
  } 
}

/*
crea_vector crea un vector con dimension n_bodies y lo llena con ceros
 */


double *crea_vector(int n_bodies){
  double *v;
  int i;
  if(!(v = malloc(n_bodies * sizeof(double)))){
    fprintf(stderr, "Problem with memory allocation\n");
    exit(1);
  }

  for(i=0;i < n_bodies;i++){
    v[i] = 0.0; 
  }
  return v;
}

