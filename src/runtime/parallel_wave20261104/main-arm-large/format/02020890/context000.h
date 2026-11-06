
extern const char native_data_020dd188[1];

typedef unsigned int size_t;

typedef long ptrdiff_t;

typedef unsigned short wchar_t;
extern const wchar_t native_data_020dd184[1];

typedef char *va_list;

typedef long long intmax_t;

enum justification_options {
    left_justification,
    right_justification,
    zero_fill
};

enum sign_options {
    only_minus,
    sign_always,
    space_holder
};

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
    long_double_argument
};

typedef struct {
    unsigned char justification_options;
    unsigned char sign_options;
    unsigned char precision_specified;
    unsigned char alternate_form;
    unsigned char argument_options;
    wchar_t conversion_char;
    int field_width;
    int precision;
} print_format;

const wchar_t *native_fn_0201f2c0(const wchar_t *,va_list *,print_format *);

wchar_t *native_fn_0201f838(long,wchar_t *,print_format);

wchar_t *native_fn_0201fa88(long long,wchar_t *,print_format);

wchar_t *native_fn_02020244(long double,wchar_t *,print_format);

wchar_t *native_fn_0201fd88(long double,wchar_t *,print_format);

wchar_t *native_fn_020212c4(const wchar_t *,wchar_t);

size_t native_fn_02021258(const wchar_t *);

wchar_t *native_fn_0201f298(const wchar_t *,wchar_t,size_t);

size_t native_fn_0201d69c(const char *);

void *native_fn_0201b21c(const void *,int,size_t);

size_t native_fn_0201b09c(wchar_t *,const char *,size_t);

int native_fn_0201b018(wchar_t *,const char *,size_t);
