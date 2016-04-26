#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/*
calcula masa que esta entre el centro y el punto
 */

double calcular_masa(double rx, double ry, double rz, double *x, double *y, double *z, int n_bodies){
  double ri = sqrt( pow(rx, 2) + pow(ry,2) + pow(rz,2));
  double rj, m;
  m = 0;

  int i;
  for(i=0; i < n_bodies; i++){
    rj = sqrt( pow(x[i], 2) + pow(y[i],2) + pow(z[i],2));
    if( rj < ri){
      m = m+1;
    }
  }
  return m;
}

double deriv_r(double t, double r, double v){
  return v;
}

double deriv_v(double t, double r, double v){
  double c = -1;
  return c*r;
}

/*
evoluciona todas las particulas en cada componente
 */

double leap_frog(double delta_t, double t, double *x, double *y, double *z, double *vx, double *vy, double *vz, double n_bodies){
  double x_in, y_in, z_in;
  double vx_in, vy_in, vz_in;
  /* for sobre cada particula */
  int i;
  for(i=0; i < n_bodies; i++){
    /*magnitud radio*/
    double r = sqrt(pow(x[i],2) + pow(y[i],2) + pow(z[i],2));
    /*kick*/
      vx_in += (0.5 * x[i])/pow(r, 3) * delta_t;
      vy_in += (0.5 * y[i])/pow(r, 3) * delta_t;
      vz_in += (0.5 * z[i])/pow(r, 3) * delta_t;
      /*drift*/
      x_in += 1.0 * vx_in * delta_t;
      y_in += 1.0 * vy_in * delta_t;
      z_in += 1.0 * vz_in * delta_t;
  }
  return 0;

}
