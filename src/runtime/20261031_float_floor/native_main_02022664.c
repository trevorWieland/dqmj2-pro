#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
double native_main_02022664(double x) {
    HIGH(x) &= 0x7fffffff;
    return x;
}
