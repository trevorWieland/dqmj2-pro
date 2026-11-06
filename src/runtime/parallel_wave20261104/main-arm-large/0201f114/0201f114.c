#include "context000.h"

unsigned long native_main_0201f114(const char *str, char **end, int base) {
    unsigned long value;
    int count, negative, overflow;
    __InStrCtrl isc;
    isc.NextChar = (char*)str;
    isc.NullCharDetected = 0;
    value = native_main_0201ed2c(base, 0x7FFFFFFF, &native_fn_0201d618 , (void*)&isc, &count, &negative, &overflow);
    if (end) {
        *end = (char*)str + count;
    }
    if (overflow) {
        value = 0xffffffffUL ;
        native_data_020ec9b0 = 34 ;
    }
    else if (negative) {
        value = -value;
    }
    return value;
}
