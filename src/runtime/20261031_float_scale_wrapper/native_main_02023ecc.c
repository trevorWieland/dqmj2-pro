extern double native_fn_02022684(double, int *);
extern double native_fn_02022740(double, int);
double native_main_02023ecc(double x, int n) {
    int exponent;
    x = native_fn_02022684(x, &exponent);
    exponent += n;
    return native_fn_02022740(x, exponent);
}
