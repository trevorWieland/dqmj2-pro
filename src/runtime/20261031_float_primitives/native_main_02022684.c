#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
double native_main_02022684(double x, int *ptr) {
    int hx, ix, lx;
    hx = HIGH(x);
    ix = 0x7FFFFFFF & hx;
    lx = LOW(x);
    *ptr = 0;

    if (ix >= 0x7FF00000 || ((ix | lx) == 0)) {
        return x;
    }

    if (ix < 0x100000) {
        x *= 1.80143985094819840000e+16;
        hx = HIGH(x);
        ix = hx & 0x7FFFFFFF;
        *ptr = -54;
    }

    *ptr += (ix >> 20) - 1022;
    hx = (hx & 0x800FFFFF) | 0x3FE00000;
    HIGH(x) = hx;
    return x;
}
