#include "context000.h"

wchar_t* native_main_02020244(long double num, wchar_t *wbuff, print_format format) {
    decimal dec;
    decform form;
    wchar_t* pw;
    char* p;
    char buff[512];
    char* q;
    int n, digits, sign;
    int int_digits, frac_digits;
    int radix_marker;
    radix_marker = '.';
    if (format.precision > 509) {
        return 0;
    }
    form.style = 0;
    form.digits = 0x20;
    native_fn_020236e8(&form, num, &dec);
    p = (char*)dec.sig.text + dec.sig.length;
    while (dec.sig.length > 1 && *--p == '0') {
        --dec.sig.length;
        ++dec.exp;
    }
    switch (*dec.sig.text) {
        case '0':
            dec.exp = 0;
            break;
        case 'I':
            if (num < 0) {
                pw = wbuff - 5;
                if (iswupper(format.conversion_char)) {
                    native_fn_02021274(pw, native_data_020dd134);
                }
                else {
                    native_fn_02021274(pw, native_data_020dd140);
                }
            }
            else {
                pw = wbuff - 4;
                if (iswupper(format.conversion_char)) {
                    native_fn_02021274(pw, native_data_020dd14c);
                }
                else {
                    native_fn_02021274(pw, native_data_020dd154);
                }
            }
            return pw;
        case 'N':
            if (dec.sign) {
                pw = wbuff - 5;
                if (iswupper(format.conversion_char)) {
                    native_fn_02021274(pw, native_data_020dd15c);
                }
                else {
                    native_fn_02021274(pw, native_data_020dd168);
                }
            }
            else {
                pw = wbuff - 4;
                if (iswupper(format.conversion_char)) {
                    native_fn_02021274(pw, native_data_020dd174);
                }
                else {
                    native_fn_02021274(pw, native_data_020dd17c);
                }
            }
            return pw;
    }
    dec.exp += dec.sig.length - 1;
    p = buff + 512;
    *--p = 0;
    switch (format.conversion_char)
    {
        case L'g':
        case L'G':
            if (dec.sig.length > format.precision) {
                native_main_02020120(&dec, format.precision);
            }
            if (dec.exp < -4 || dec.exp >= format.precision)
            {
                if (format.alternate_form) {
                    --format.precision;
                }
                else {
                    format.precision = dec.sig.length - 1;
                }
                if (format.conversion_char == L'g') {
                    format.conversion_char = L'e';
                }
                else {
                    format.conversion_char = L'E';
                }
                goto e_format;
            }
            if (format.alternate_form) {
                format.precision -= dec.exp + 1;
            }
            else {
                if ((format.precision = dec.sig.length - (dec.exp + 1)) < 0) {
                    format.precision = 0;
                }
            }
            goto f_format;
        case L'e':
        case L'E':
        e_format:
            if (dec.sig.length > format.precision + 1) {
                native_main_02020120(&dec, format.precision + 1);
            }
            n = dec.exp;
            sign = '+';
            if (n < 0) {
                n = -n;
                sign = '-';
            }
            for (digits = 0; n || digits < 2; ++digits) {
                *--p = n % 10 + '0';
                n /= 10;
            }
            *--p = sign;
            *--p = format.conversion_char;
            if (buff - p + format.precision > 509) {
                return 0;
            }
            if (dec.sig.length < format.precision + 1) {
                for (n = format.precision + 1 - dec.sig.length + 1; --n;) {
                    *--p = '0';
                }
            }
            for (n = dec.sig.length, q = (char*)dec.sig.text + dec.sig.length; --n;) {
                *--p = *--q;
            }
            if (format.precision || format.alternate_form) {
                *--p = radix_marker;
            }
            *--p = *dec.sig.text;
            if (dec.sign)
                *--p = '-';
            else if (format.sign_options == sign_always)
                *--p = '+';
            else if (format.sign_options == space_holder)
                *--p = ' ';
            break;
        case L'f':
        case L'F':
        f_format:
            if ((frac_digits = -dec.exp + dec.sig.length - 1) < 0)
                frac_digits = 0;
            if (frac_digits > format.precision) {
                native_main_02020120(&dec, dec.sig.length - (frac_digits - format.precision));
                if ((frac_digits = -dec.exp + dec.sig.length - 1) < 0)
                    frac_digits = 0;
            }
            if ((int_digits = dec.exp + 1) < 0)
                int_digits = 0;
            if (int_digits + frac_digits > 509)
                return 0;
            q = (char *) dec.sig.text + dec.sig.length;
            for (digits = 0; digits < (format.precision - frac_digits); ++digits)
                *--p = '0';
            for (digits = 0; digits < frac_digits && digits < dec.sig.length; ++digits)
                *--p = *--q;
            for (; digits < frac_digits; ++digits)
                *--p = '0';
            if (format.precision || format.alternate_form)
                *--p = radix_marker;
            if (int_digits) {
                for (digits = 0; digits < int_digits - dec.sig.length; ++digits) {
                    *--p = '0';
                }
                for (; digits < int_digits; ++digits) {
                    *--p = *--q;
                }
            }
            else {
                *--p = '0';
            }
            if (dec.sign) {
                *--p = '-';
            }
            else if (format.sign_options == sign_always) {
                *--p = '+';
            }
            else if (format.sign_options == space_holder) {
                *--p = ' ';
            }
            break;
    }
    pw = wbuff - native_fn_0201d69c(p) - 1;
    native_fn_0201b09c(pw, p, native_fn_0201d69c(p));
    return pw;
}
