#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
int native_main_02023e48(double dbl) {
    return (HIGH(dbl)) & 0x80000000;
}
