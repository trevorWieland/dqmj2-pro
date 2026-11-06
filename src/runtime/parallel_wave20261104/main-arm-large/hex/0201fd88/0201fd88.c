#include "context000.h"

wchar_t * native_main_0201fd88(long double num, wchar_t * buff, print_format format)  {
    wchar_t *p;
    unsigned char *q;
    unsigned char working_byte;
    long double ld;
    int expbits, expmask;
    unsigned snum;
    long exp;
    print_format exp_format;
    int hex_precision;
    int mantissa_bit;
    decform form;
    decimal dec;
    int radix_marker;
    radix_marker = 46;
    p = buff;
    ld = num;
    if (format.precision > 509) {
        return 0;
    }
    form.style = (char)0;
    form.digits = 0x20;
    native_fn_020236e8(&form, num, &dec);
    if (native_fn_02022664(num) == 0.0) {p = buff - 6;native_fn_02021274(p,native_data_020dd128);return p;}
    if (*dec.sig.text == 'I') {
            if (dec.sign) {
                p = buff - 5;
                if (format.conversion_char == L'A') native_fn_02021274(p, native_data_020dd134);
                else native_fn_02021274(p, native_data_020dd140);
            } else {
                p = buff - 4;
                if (format.conversion_char == L'A') native_fn_02021274(p, native_data_020dd14c);
                else native_fn_02021274(p, native_data_020dd154);
            }
            return p;
    } else if (*dec.sig.text == 'N') {
            if (dec.sign) {
                p = buff - 5;
                if (format.conversion_char == L'A') native_fn_02021274(p, native_data_020dd15c);
                else native_fn_02021274(p, native_data_020dd168);
            } else {
                p = buff - 4;
                if (format.conversion_char == L'A') native_fn_02021274(p, native_data_020dd174);
                else native_fn_02021274(p, native_data_020dd17c);
            }
            return p;
    }
    exp_format.justification_options = 1;
    exp_format.sign_options = 1;
    exp_format.precision_specified = 0;
    exp_format.alternate_form = 0;
    exp_format.argument_options = 0;
    exp_format.field_width = 0;
    exp_format.precision = 1;
    exp_format.conversion_char = 'd';
    expbits = 11;
    expmask = 0x7FF;
    {int i;char c;char *bytes=(char *)&num;for(i=0;i<4;i++){c=bytes[i];bytes[i]=bytes[7-i];bytes[7-i]=c;}}
    snum = ((unsigned char *)&num)[0] << 25;
    if ((64 - (53 - 1) - 1) > 7)
        snum |= ((unsigned char *)&num)[1] << 17;
    if ((64 - (53 - 1) - 1) > 15)
        snum |= ((unsigned char *)&num)[2] << 9;
    if ((64 - (53 - 1) - 1) > 23)
        snum |= ((unsigned char *)&num)[3] << 1;
    snum = (snum >> (32 - expbits)) & expmask;
    exp = snum - 0x3FF;
    p = native_fn_0201f838(exp, buff, exp_format);
    if (format.conversion_char == L'a')
        *--p = L'p';
    else
        *--p = L'P';
    q = (unsigned char *)&num;
    if (1 ) {
        mantissa_bit = (1 + expbits + format.precision * 4) - 1;
    }
    else {
        mantissa_bit = (1 + expbits + format.precision * 4) - 4;
    }
    for (hex_precision = format.precision; hex_precision >= 1; hex_precision--) {
        if (mantissa_bit < 64) {
            int mantissa_byte;
            mantissa_byte = mantissa_bit >> 3;
            working_byte = (*(q + mantissa_byte)) >> (7 - (mantissa_bit & 7));
            if ((mantissa_bit & ~7) != ((mantissa_bit - 4) & ~7)) {
                working_byte |= ((*(q + (mantissa_byte - 1))) << 8) >> (7 - ((mantissa_bit) & 7));
            }
            if (!1 ) {
                if (mantissa_bit == 1 + expbits) {
                    *--p = radix_marker;
                    working_byte &= 0x1;
                }
            }
            if ((working_byte &= 0xF) < 10) {
                working_byte += L'0';
            }
            else
                if (format.conversion_char == L'a') {
                    working_byte += L'a' - 10;
                }
                else {
                    working_byte += L'A' - 10;
                }
        }
        else {
            working_byte = L'0';
        }
        *--p = working_byte;
        mantissa_bit -= 4;
    }
    if (1 ){
        if (format.precision || format.alternate_form) {
            *--p = radix_marker;
        }
        *--p = '1';
    }
    if (format.conversion_char == L'a') {
        *--p = L'x';
    }
    else {
        *--p = L'X';
    }
    *--p = L'0';
    if (dec.sign) {
        *--p = L'-';
    }
    else if (format.sign_options == sign_always) {
        *--p = L'+';
    }
    else if (format.sign_options == space_holder) {
        *--p = L' ';
    }
    return p;
}
