#include "context000.h"

wchar_t* native_main_0201fa88(long long num, wchar_t *pBuf, print_format fmt) {
    unsigned long long unsigned_num, base;
    wchar_t* p;
    int n, digits;
    int minus = 0;
    unsigned_num = num;
    minus = 0;
    p = pBuf;
    *--p = 0;
    digits = 0;
    if (!num && !fmt.precision && !(fmt.alternate_form && fmt.conversion_char == L'o')) {
        return p;
    }
    switch (fmt.conversion_char) {
        case L'd':
        case L'i':
            base = 10;
            if (num < 0) {
                if (num != 0x8000000000000000) {
                    unsigned_num = -num;
                }
                minus = 1;
            }
            break;
        case L'o':
            base = 8;
            fmt.sign_options = only_minus;
            break;
        case L'u':
            base = 10;
            fmt.sign_options = only_minus;
            break;
        case L'x':
        case L'X':
            base = 16;
            fmt.sign_options = only_minus;
            break;
    }
    do {
        n = native_fn_020260e8(unsigned_num, base);
        unsigned_num = native_fn_020260dc(unsigned_num, base);
        if (n < 10) {
            n += L'0';
        }
        else {
            n -= 10;
            if (fmt.conversion_char == L'x') {
                n += L'a';
            }
            else {
                n += L'A';
            }
        }
        *--p = n;
        ++digits;
    } while (unsigned_num != 0);
    if (base == 8 && fmt.alternate_form && *p != L'0') {
        *--p = L'0';
        ++digits;
    }
    if (fmt.justification_options == zero_fill) {
        fmt.precision = fmt.field_width;
        if (minus || fmt.sign_options != only_minus) {
            --fmt.precision;
        }
        if (base == 16 && fmt.alternate_form) {
            fmt.precision -= 2;
        }
    }
    if (pBuf - p + fmt.precision > 509) {
        return 0;
    }
    while (digits < fmt.precision) {
        *--p = L'0';
        ++digits;
    }
    if (base == 16 && fmt.alternate_form) {
        *--p = fmt.conversion_char;
        *--p = L'0';
    }
    if (minus) {
        *--p = L'-';
    }
    else if (fmt.sign_options == sign_always) {
        *--p = L'+';
    }
    else if (fmt.sign_options == space_holder) {
        *--p = L' ';
    }
    return p;
}
