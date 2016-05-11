void escribe_estado(double *x, double *y, double *U, double *K, int n, int id);
void posiciones_iniciales(double *p, int n);
double *crea_vector(int n);
int *crea_vector_int(int n);
void recibe_input(int argc, char **argv, int *n, double *e, int *num_buckets, int *num_threads);