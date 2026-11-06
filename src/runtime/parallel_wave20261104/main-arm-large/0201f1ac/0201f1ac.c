#include "context000.h"

long native_main_0201f1ac(const char *str, char **end, int base) {
    unsigned long uvalue;
    long svalue;
    int count, negative, overflow;
    __InStrCtrl isc;
    isc.NextChar = (char*)str;
    isc.NullCharDetected = 0;
    uvalue = native_main_0201ed2c(base, 0x7FFFFFFF, &native_fn_0201d618 , (void*)&isc, &count, &negative, &overflow);
    if (end) {
        *end = (char*)str + count;
    }
    if (overflow || (!negative && uvalue > 2147483647L ) || (negative && uvalue > -(-2147483647L-1) )) {
        svalue = (negative ? -(-2147483647L-1) : 2147483647L );
        native_data_020ec9b0 = 34 ;
    }
    else {
        svalue = (negative ? (long)-uvalue : (long)uvalue);
    }
    return svalue;
}
