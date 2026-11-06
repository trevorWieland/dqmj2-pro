typedef unsigned short wchar_t;

unsigned long long native_fn_020260e8(unsigned long long,unsigned long long);

unsigned long long native_fn_020260dc(unsigned long long,unsigned long long);

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

wchar_t* native_main_0201fa88(long long num, wchar_t *pBuf, print_format fmt);
