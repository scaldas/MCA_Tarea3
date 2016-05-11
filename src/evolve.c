#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "omp.h"
#define PI 3.141592653589793238462643383
#define G_GRAV 4.49E-3

double calcula_tiempo_total(int n){
  double t_dyn;
  double rho;
  double R;
  R = pow(n, 1.0/3.0);
  rho = n / (4.0/3.0) / (PI * pow(R,3));
  t_dyn = 1.0/sqrt(G_GRAV * rho);
  return 5 * t_dyn;
}

double calcula_time_step(int n, double epsilon){
  double t_dyn; 
  double rho;
  double R;
  rho = n / (4.0/3.0) / (PI * pow(epsilon, 3));
  t_dyn = 1.0/sqrt(G_GRAV * rho);
  return t_dyn;
}

void calcula_energia(double *p, double *v, double *U, double *K, int n){
  int i, j, k;
  double delta_total;
  for(i=0;i<n;i++){
    K[i] = 0.0;
    for(k=0;k<3;k++){
      K[i] += 0.5 * pow(v[3*i + k],2.0);
    }
    U[i] = 0.0;
    for(j=0;j<n;j++){
      if(i!=j){
	delta_total = 0.0;
	for(k=0;k<3;k++){
	  delta_total += pow((p[i*3 + k] - p[j*3 + k]),2);
	}      
	U[i] += -G_GRAV/sqrt(delta_total);
      }
    }
  }
}

double calcula_masa(int num_bucket, double *buckets_masses) {
  double m;
  int i;

  m = 0.0;
  for(i = 0 ; i < num_bucket ; i++){
    m += buckets_masses[i];
  }

  return m;
}

void calcula_aceleracion(
    double *p, double *a, int n, double epsilon, int *buckets, double *buckets_masses){
  int i,k;
  double delta, delta_total;
  double m, r_mag;
#pragma omp parallel for private(k, m, r_mag), shared(buckets, buckets_masses, p, a)
  for (i = 0 ; i < n ; i++) {
    r_mag = 0.0;
    for (k = 0 ; k < 3 ; k++) {
      r_mag += pow(p[i*3 + k], 2);
    }

    m = calcula_masa(buckets[i], buckets_masses);

    for (k = 0 ; k < 3 ; k++) {
      a[i*3 + k] = -G_GRAV * m * p[i*3 + k]/pow((r_mag + pow(epsilon,2)), 3.0/2.0);
    }
  }
}


void  kick(double *p, double *v, double *a, int n, double delta_t){
  int i,k;

  for(i = 0 ; i < n ; i++){
    for(k = 0 ; k < 3 ; k++){
      v[i*3 + k] += a[i*3 + k] * delta_t;
    }
  }
}  

void  drift(double *p, double *v, double *a, int n, double delta_t){
  int i,k;
  for(i = 0 ; i < n ; i++){
    for(k = 0 ; k < 3 ; k++){
      p[i*3 + k] += v[i*3 + k] * delta_t;
    }
  }
}  

void asigna_buckets(double *p, int n, int *buckets, double *buckets_masses, int num_buckets){
  double R, r, bucket_id;
  int i, k;
  R = pow(n, 1.0/3.0);

  for(i = 0 ; i < 10*num_buckets ; i++) {
    buckets_masses[i] = 0.0;
  }

  for(i = 0 ; i < n ; i++){
    r = 0.0;
    for(k = 0 ; k < 3 ; k++) {
      r += pow(p[i*3 + k], 2);
    }
    r = sqrt(r);

    bucket_id = (int)(r/(R/num_buckets));
    buckets[i] = (bucket_id < 10*num_buckets)? bucket_id : 10*num_buckets - 1;
    /*if(buckets[i] < 0) {
      printf("%d\n", buckets[i]);
      printf("%e\n", r/(R/num_buckets));
      printf("%e\n", (R/num_buckets));
      printf("%e\n", r);
      printf("%e\n", p[i*3 + 0]);
      printf("%e\n", p[i*3 + 1]);
      printf("%e\n", p[i*3 + 2]);
    }*/
    buckets_masses[buckets[i]]++;
  }
}

