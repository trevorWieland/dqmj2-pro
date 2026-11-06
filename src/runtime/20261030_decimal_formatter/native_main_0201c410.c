typedef unsigned int size_t;
typedef long ptrdiff_t;
typedef long long intmax_t;
typedef unsigned short wchar_t;
typedef char *va_list;
enum justification_options { left_justification, right_justification, zero_fill };
enum sign_options { only_minus, sign_always, space_holder };
enum argument_options {
    normal_argument,
    char_argument,
    short_argument,
    long_argument,
    long_long_argument,
    wchar_argument,
    intmax_argument,
    size_t_argument,
    ptrdiff_argument,
    long_double_argument,
};
typedef struct {
    unsigned char justification_options;
    unsigned char sign_options;
    unsigned char precision_specified;
    unsigned char alternate_form;
    unsigned char argument_options;
    unsigned char conversion_char;
    int field_width;
    int precision;
} print_format;
typedef char NdsIntegerFormatterAbi[(sizeof(long) == 4 && sizeof(void *) == 4 && sizeof(print_format) == 16) ? 1 : -1];
typedef struct { char sign; short exp; struct { unsigned char length; unsigned char text[32]; } sig; } decimal;
typedef struct { char style; short digits; } decform;
typedef char DecimalFormatAbi[(sizeof(long double) == 8 && sizeof(decimal) == 38 && sizeof(decform) == 4) ? 1 : -1];
extern void native_fn_020236e8(const decform *, long double, decimal *);
extern void native_fn_0201c2ec(decimal *, int);
typedef struct { char text[4]; } text4;
typedef struct { char text[5]; } text5;
extern const unsigned short native_data_020d8e04[128];
extern const char native_data_020dd0ec[5];
extern const char native_data_020dd0f4[5];
extern const char native_data_020dd0fc[4];
extern const char native_data_020dd100[4];
extern const char native_data_020dd104[5];
extern const char native_data_020dd10c[5];
extern const char native_data_020dd114[4];
extern const char native_data_020dd118[4];
static inline int isupper(int c) { return (c < 0 || c >= 128) ? 0 : (native_data_020d8e04[c] & 0x200); }
extern void *__memcpy(void *, const void *, unsigned long);
char* native_main_0201c410(long double num, char* buff, print_format format) {
    decimal dec;
    decform form;
    char* p;
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
            p = buff - 5;

            if (isupper(format.conversion_char)) {
                __memcpy(p, native_data_020dd0ec, 5);
            } else {
                __memcpy(p, native_data_020dd0f4, 5);
            }
        } else {
            p = buff - 4;
            if (isupper(format.conversion_char)) {
                __memcpy(p, native_data_020dd0fc, 4);
            } else {
                __memcpy(p, native_data_020dd100, 4);
            }
        }

        return p;

    case 'N':
        if (dec.sign) {
            p = buff - 5;

            if (isupper(format.conversion_char)) {
                __memcpy(p, native_data_020dd104, 5);
            } else {
                __memcpy(p, native_data_020dd10c, 5);
            }
        } else {
            p = buff - 4;
            if (isupper(format.conversion_char)) {
                __memcpy(p, native_data_020dd114, 4);
            } else {
                __memcpy(p, native_data_020dd118, 4);
            }
        }

        return p;
    }

    dec.exp += (dec.sig.length - 1);

    p = buff;
    *--p = 0;

    switch (format.conversion_char) {
    case 'g':
    case 'G':

        if (dec.sig.length > format.precision) {
            native_fn_0201c2ec(&dec, format.precision);
        }

        if (dec.exp < -4 || dec.exp >= format.precision) {
            if (format.alternate_form) {
                --format.precision;
            } else {
                format.precision = dec.sig.length - 1;
            }

            if (format.conversion_char == 'g') {
                format.conversion_char = 'e';
            } else {
                format.conversion_char = 'E';
            }

            goto e_format;
        }

        if (format.alternate_form) {
            format.precision -= dec.exp + 1;
        } else {
            if ((format.precision = dec.sig.length - (dec.exp + 1)) < 0) {
                format.precision = 0;
            }
        }

        goto f_format;

    case 'e':
    case 'E':
    e_format:

        if (dec.sig.length > format.precision + 1) {
            native_fn_0201c2ec(&dec, format.precision + 1);
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

    case 'f':
    case 'F':
    f_format:

        if ((frac_digits = -dec.exp + dec.sig.length - 1) < 0)
            frac_digits = 0;

        if (frac_digits > format.precision) {
            native_fn_0201c2ec(&dec, dec.sig.length - (frac_digits - format.precision));

            if ((frac_digits = -dec.exp + dec.sig.length - 1) < 0)
                frac_digits = 0;
        }

        if ((int_digits = dec.exp + 1) < 0)
            int_digits = 0;

        if (int_digits + frac_digits > 509)
            return 0;

        q = (char*)dec.sig.text + dec.sig.length;

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
        } else {
            *--p = '0';
        }

        if (dec.sign) {
            *--p = '-';
        } else if (format.sign_options == sign_always) {
            *--p = '+';
        } else if (format.sign_options == space_holder) {
            *--p = ' ';
        }

        break;
    }

    return p;
}
