double calcular_masa(double rx, double ry, double rz, double *x, double *y, double *z, int n_bodies);
double deriv_r(double t, double r, double v);
double deriv_v(double t, double r, double v, double rx, double ry, double rz, double *x, double *y, double *z, double n_bodies);
double leap_frog(double delta_t, double t, double *x, double *y, double *z, double *vx, double *vy, double *vz, double n_bodies);
void escribe_estado(double *x, double *y, double *z, int n_bodies, int id);
void evoluciona_sistema(double t_total, double delta_t, double *x, double *y, double *z, double *vx, double *vy, double *vz, double n_bodies);
