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
extern unsigned long long native_fn_020260e8(unsigned long long, unsigned long long);
extern unsigned long long native_fn_020260dc(unsigned long long, unsigned long long);
typedef char NdsLonglongFormatterAbi[(sizeof(long long) == 8 && sizeof(long) == 4 && sizeof(void *) == 4 && sizeof(print_format) == 16) ? 1 : -1];
char* native_main_0201bb14(signed long long num, char* pBuf, print_format fmt) {
    unsigned long long unsigned_num, base;
    char* p;
    int n, digits;
    int minus = 0;
    unsigned_num = num;
    minus = 0;
    p = pBuf;
    *--p = 0;
    digits = 0;
    if (!num && !fmt.precision && !(fmt.alternate_form && fmt.conversion_char == 'o')) {
        return p;
    }
    switch (fmt.conversion_char) {
    case 'd':
    case 'i':
        base = 10;
        if (num < 0) {
            if (num != 0x8000000000000000LL)
                unsigned_num = -unsigned_num;
            minus = 1;
        }
        break;
    case 'o':
        base = 8;
        fmt.sign_options = only_minus;
        break;
    case 'u':
        base = 10;
        fmt.sign_options = only_minus;
        break;
    case 'x':
    case 'X':
        base = 16;
        fmt.sign_options = only_minus;
        break;
    }
    do {
        n = native_fn_020260e8(unsigned_num, base);
        unsigned_num = native_fn_020260dc(unsigned_num, base);
        if (n < 10) {
            n += '0';
        } else {
            n -= 10;
            if (fmt.conversion_char == 'x') {
                n += 'a';
            } else {
                n += 'A';
            }
        }
        *--p = n;
        ++digits;
    } while (unsigned_num != 0);
    if (base == 8 && fmt.alternate_form && *p != '0') {
        *--p = '0';
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
        *--p = '0';
        ++digits;
    }
    if (base == 16 && fmt.alternate_form) {
        *--p = fmt.conversion_char;
        *--p = '0';
    }
    if (minus) {
        *--p = '-';
    } else if (fmt.sign_options == sign_always) {
        *--p = '+';
    } else if (fmt.sign_options == space_holder) {
        *--p = ' ';
    }
    return p;
}
