#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "iniciar.h"

int main(int argc, char **argv){

  int i = 0;
  int n_bodies = 0;
  double epsilon = 0;
  double *x = NULL, *y = NULL, *z = NULL; //Vectores posicion
  double *v_x = NULL, *v_y = NULL, *v_z = NULL;  //Vectores velocidad
  double *a_x = NULL, *a_y = NULL, *a_z = NULL;  //Vectores aceleracion

  //Inicializacion de vectores
  recibe_input(argc, argv, &n_bodies, &epsilon);
  x = crea_vector(n_bodies);
  y = crea_vector(n_bodies);
  z = crea_vector(n_bodies);
  v_x = crea_vector(n_bodies);
  v_y = crea_vector(n_bodies);
  v_z = crea_vector(n_bodies);
  a_x = crea_vector(n_bodies);
  a_y = crea_vector(n_bodies);
  a_z = crea_vector(n_bodies);  

  init_positions(x, y, z, n_bodies); 
/* 
  for(i=0 ; i<n_bodies ; i++){

    printf("%f \t %f \t %f \n",  x[i],  y[i],  z[i]);

  }
 */ 
  return 0;
}
