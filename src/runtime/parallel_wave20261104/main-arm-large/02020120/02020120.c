#include "context000.h"

void native_main_02020120(decimal *dec, int new_length) {
    char c;
    char* p;
    int carry;
    if (new_length < 0) {
return_zero:
        dec->exp = 0;
        dec->sig.length = 1;
        *dec->sig.text = '0';
        return;
    }
    if (new_length >= dec->sig.length) {
        return;
    }
    p = (char*)dec->sig.text + new_length + 1;
    c = *--p - L'0';
    if (c == 5) {
        char* q = &((char*)dec->sig.text)[dec->sig.length];
        while (--q > p && *q == '0');
        carry = (q == p) ? p[-1] & 1 : 1;
    }
    else {
        carry = (c > 5);
    }
    while (new_length != 0) {
        c = *--p - L'0' + carry;
        if ((carry = (c > 9)) != 0 || c == 0) {
            --new_length;
        }
        else {
            *p = c + L'0';
            break;
        }
    }
    if (carry != 0) {
        dec->exp += 1;
        dec->sig.length = 1;
        *dec->sig.text = '1';
        return;
    }
    else if (new_length == 0) {
        goto return_zero;
    }
    dec->sig.length = new_length;
}
