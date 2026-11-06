#define HIGH(x) (((int *)&(x))[1])
#define LOW(x) (((int *)&(x))[0])
int native_main_02023e5c(double dbl) {
    switch ((HIGH(dbl)) & 0x7FF00000) {
        case 0x7FF00000:
            if (((HIGH(dbl)) & 0xFFFFF) || (LOW(dbl)) & 0xFFFFFFFF) {
                return 1;
            }
            else {
                return 2;
            }

            break;
        case 0:
            if (((HIGH(dbl)) & 0xFFFFF) || (LOW(dbl)) & 0xFFFFFFFF) {
                return 5;
            }
            else {
                return 3;
            }

            break;
    }

    return 4;
}
