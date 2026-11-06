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
extern long double native_fn_02022664(long double);
extern char *native_fn_0201b8c8(long, char *, print_format);
extern const char native_data_020dd0e4[6];
#define TARGET_FLOAT_EXP_BITS 11
#define TARGET_FLOAT_IMPLICIT_J_BIT 1
char* native_main_0201be10(long double num, char* buff, print_format format) {

    char *p;
    unsigned char *q;
    unsigned char working_byte;
    long double ld;
    int swap_index;
    char swap_byte;
    char *swap_bytes;
    int expbits, expmask;
    unsigned snum;
    long exp;
    print_format exp_format;
    int hex_precision;
    int mantissa_bit;
    decform form;
    decimal dec;
    int radix_marker;
    
    radix_marker = '.';
    p = buff;
    ld = num;

    
    if (format.precision > 509) {
        return 0;
    }

    form.style = (char)0;
    form.digits = 0x20;
    native_fn_020236e8(&form, ld, &dec);
    if (native_fn_02022664(num) == 0.0) {
        p = buff - 6;
        __memcpy(p, native_data_020dd0e4, 6);
        return p;
    }

    if (*dec.sig.text == 'I') {
            if (dec.sign) {
                p = buff - 5;
                if (format.conversion_char == 'A') __memcpy(p, native_data_020dd0ec, 5);
                else __memcpy(p, native_data_020dd0f4, 5);
            }
            else {
                p = buff - 4;
                if (format.conversion_char == 'A') __memcpy(p, native_data_020dd0fc, 4);
                else __memcpy(p, native_data_020dd100, 4);
            }
        
            return p;
    } else if (*dec.sig.text == 'N') {
            if (dec.sign) {
                p = buff - 5;
                if (format.conversion_char == 'A') __memcpy(p, native_data_020dd104, 5);
                else __memcpy(p, native_data_020dd10c, 5);
            }
            else {
                p = buff - 4;
                if (format.conversion_char == 'A') __memcpy(p, native_data_020dd114, 4);
                else __memcpy(p, native_data_020dd118, 4);
            }
            
            return p;
    }

    exp_format.justification_options = right_justification;
    exp_format.sign_options = sign_always;
    exp_format.precision_specified = 0;
    exp_format.alternate_form = 0;
    exp_format.argument_options = normal_argument;
    exp_format.field_width = 0;
    exp_format.precision = 1;
    exp_format.conversion_char = 'd';

    swap_bytes = (char *)&num;
    for (swap_index = 0; swap_index < 4; ++swap_index) {
        swap_byte = swap_bytes[swap_index];
        swap_bytes[swap_index] = swap_bytes[7 - swap_index];
        swap_bytes[7 - swap_index] = swap_byte;
    }
    expbits = 11;
    expmask = 0x7FF;

    snum = ((unsigned char *)&num)[0] << 25;
    if (TARGET_FLOAT_EXP_BITS > 7)
        snum |= ((unsigned char *)&num)[1] << 17;
    if (TARGET_FLOAT_EXP_BITS > 15)
        snum |= ((unsigned char *)&num)[2] << 9;
    if (TARGET_FLOAT_EXP_BITS > 23)
        snum |= ((unsigned char *)&num)[3] << 1;

    snum = (snum >> (32 - expbits)) & expmask;

    exp = snum - 0x3FF;

    p = native_fn_0201b8c8(exp, buff, exp_format);
    if (format.conversion_char == 'a')
        *--p = 'p';
    else
        *--p = 'P';
    q = (unsigned char *)&num;

    if (TARGET_FLOAT_IMPLICIT_J_BIT) {
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
                working_byte |= (((*(q + (mantissa_byte - 1))) << 8) >> (7 - ((mantissa_bit) & 7)));
            }

            if (!TARGET_FLOAT_IMPLICIT_J_BIT) {
                if (mantissa_bit == 1 + expbits) {
                    *--p = radix_marker;
                    working_byte &= 0x1;
                }
            }
            
            if ((working_byte &= 0xF) < 10) {
                working_byte += (unsigned char)'0';
            }
            else
                if (format.conversion_char == 'a') {
                    working_byte += (unsigned char)('a' - 10);
                }
                else {
                    working_byte += (unsigned char)('A' - 10);
                }
        }
        else {
            working_byte = '0';
        }

        *--p = working_byte;
        mantissa_bit -= 4;
    }
    
    if (TARGET_FLOAT_IMPLICIT_J_BIT){
        if (format.precision || format.alternate_form) {
            *--p = radix_marker;
        }

        *--p = '1';
    }

    if (format.conversion_char == 'a') {
        *--p = 'x';
    }
    else {
        *--p = 'X';
    }

    *--p = '0';

    if (dec.sign) {
        *--p = '-';
    }
    else if (format.sign_options == sign_always) {
        *--p = '+';
    }
    else if (format.sign_options == space_holder) {
        *--p = ' ';
    }

    return p;
}
