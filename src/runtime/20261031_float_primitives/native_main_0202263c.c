#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
double native_main_0202263c(double x, double y) {
    HIGH(x) = (HIGH(x)) & 0x7FFFFFFF | (HIGH(y)) & 0x80000000;
    return x;
}
