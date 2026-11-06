#include "context000.h"

void native_main_02022a94(decimal *pDecimal, unsigned long long input) {
    pDecimal->sign = 0;
    pDecimal->sig.length = 0;
    for (; input != 0; input = native_fn_020260dc(input, 10)) {
        unsigned char index = pDecimal->sig.length++;
        pDecimal->sig.text[index] = (unsigned char)(native_fn_020260e8(input, 10));
    }
    {
        unsigned char* start = pDecimal->sig.text;
        unsigned char* end = pDecimal->sig.text + pDecimal->sig.length;
        for (; start < --end; ++start) {
            unsigned char t = *start;
            *start = *end;
            *end = t;
        }
    }
    pDecimal->exponent = (short)(pDecimal->sig.length - 1);
}
