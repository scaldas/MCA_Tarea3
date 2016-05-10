#include <stdio.h>
#include <stdlib.h>
#include "inicial.h"
#include "evolve.h"
/*
  Un programa sencillo para seguir la evolucion
  dinamica de un conjunto de N masas puntuales.
*/

int main(int argc, char **argv){
  int i=0, N=0, num_buckets;
  double *p=NULL;
  double *v=NULL;
  double *a=NULL;
  double *U=NULL;
  double *K=NULL;
  int *buckets;
  double *buckets_masses;
  double time_step=0, total_time=0, epsilon=0;
  int n_steps=0;

  /*inicializacion*/
  recibe_input(argc, argv, &N, &epsilon, &num_buckets);
  p = crea_vector(3*N);
  v = crea_vector(3*N);
  a = crea_vector(3*N);
  U = crea_vector(N);
  K = crea_vector(N);
  buckets = crea_vector_int(N);
  buckets_masses = crea_vector(10*num_buckets);

  posiciones_iniciales(p, N);
  calcula_energia(p, v, U, K, N);
  escribe_estado(p, v, U, K, N, i);
  
  // tiempos caracteristicos 
  total_time = calcula_tiempo_total(N);
  time_step = calcula_time_step(N, epsilon);
  n_steps = (int)(total_time/time_step);
  fprintf(stderr, "tiempo total: %f time_step: %f n_steps %d\n", total_time, time_step, n_steps);
  
  //evolucion temporal
  asigna_buckets(p, N, buckets, buckets_masses, num_buckets);
  calcula_aceleracion(p, a, N, epsilon, buckets, buckets_masses);
  kick(p, v, a, N, time_step/2.0);  
  for(i = 0 ; i < n_steps ; i++) {
    drift(p, v, a, N, time_step); 
    asigna_buckets(p, N, buckets, buckets_masses, num_buckets);
    calcula_aceleracion(p, a, N, epsilon, buckets, buckets_masses);
    kick(p, v, a, N, time_step);  
  }
  calcula_energia(p, v, U, K, N);
  escribe_estado(p, v, U, K, N, i);    
  return 0;
}

