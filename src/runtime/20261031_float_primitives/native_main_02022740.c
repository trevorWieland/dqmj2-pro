#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
extern int native_fn_02023e5c(double);
extern double native_fn_0202263c(double,double);

double native_main_02022740(double x, int n) {
    int exp, hx, lx;

    if (!(native_fn_02023e5c(x) > 2) || x == 0.0) {
        return x;
    }

    hx = HIGH(x);
    lx = LOW(x);
    exp = (hx & 0x7FF00000) >> 20;

    if (exp == 0) {
        if ((lx | (hx & 0x7FFFFFFF)) == 0) {
            return x;
        }

        x *= 1.80143985094819840000e+16;
        hx = HIGH(x);
        exp = ((hx & 0x7FF00000) >> 20) - 54;

        if (n < -50000) {
            return 1.0e-300 * x;
        }
    }

    if (exp == 0x7FF) {
        return x + x;
    }

    exp = exp + n;
    
    if (exp > 0x7FE) {
        return 1.0e+300 * native_fn_0202263c(1.0e+300, x);
    }

    if (exp > 0) {
        HIGH(x) = (hx & 0x800FFFFF)| (exp << 20);
        return x;
    }

    if (exp <= -54) {
        if (n > 50000) {
            return 1.0e+300 * native_fn_0202263c(1.0e+300, x);
        }
        else {
            return 1.0e-300 * native_fn_0202263c(1.0e-300, x);
        }
    }

    exp += 54;
    HIGH(x) = (hx & 0x800FFFFF) | (exp << 20);
    return x * 5.55111512312578270212e-17;
}
