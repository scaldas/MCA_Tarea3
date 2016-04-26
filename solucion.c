#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#define G_GRAV 4.49E-3

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

double deriv_v(double t, double r, double v, double rx, double ry, double rz, double *x, double *y, double *z, double n_bodies){
  double m = calcular_masa(rx, ry, rz, x, y, z, n_bodies);
  double r_mag = sqrt( pow(rx, 2) + pow(ry, 2) + pow(rz, 2));
  return (-G*m*r)/ pow(r_mag, 3);
}

/*
evoluciona todas las particulas en cada componente
 */

double leap_frog(double delta_t, double t, double *x, double *y, double *z, double *vx, double *vy, double *vz, double n_bodies){
  double x_in, y_in, z_in;
  double vx_in, vy_in, vz_in;
  double m_temp;
  /* for sobre cada particula */
  int i;
  for(i=0; i < n_bodies; i++){
    /*magnitud radio*/
    /*kick*/
    double deriv_vx = deriv_v(t, x[i], vx[i], x[i], y[i], z[i], x, y, z);
    double deriv_vy = deriv_v(t, y[i], vy[i], x[i], y[i], z[i], x, y, z);
    double deriv_vz = deriv_v(t, z[i], vz[i], x[i], y[i], z[i], x, y, z);
      vx_in += 0.5 * deriv_vx * delta_t;
      vy_in += 0.5 * deriv_vy * delta_t;
      vz_in += 0.5 * deriv_vz * delta_t;
      /*drift*/
      x_in += 1.0 * vx_in * delta_t;
      y_in += 1.0 * vy_in * delta_t;
      z_in += 1.0 * vz_in * delta_t;
      /*kick*/
      deriv_vx = deriv_v(t, x_in, vx_in, x[i], y[i], z[i], x, y, z);
      deriv_vy = deriv_v(t, y_in, vy_in, x[i], y[i], z[i], x, y, z);
      deriv_vz = deriv_v(t, z_in, vz_in, x[i], y[i], z[i], x, y, z);

  }
  return 0;

}
