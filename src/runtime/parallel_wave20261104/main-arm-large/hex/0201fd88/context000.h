typedef unsigned short wchar_t;

double native_fn_02022664(double);

typedef struct decimal {char sign;char pad1;short exp;struct {unsigned char length;unsigned char text[32];unsigned char pad37;} sig;} decimal;

typedef struct decform {char style;char pad1;short digits;} decform;

void native_fn_020236e8(const decform *,double,decimal *);

wchar_t *native_fn_02021274(wchar_t *,const wchar_t *);

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

wchar_t *native_fn_0201f838(long,wchar_t *,print_format);

extern const wchar_t native_data_020dd128[6];

extern const wchar_t native_data_020dd134[5];

extern const wchar_t native_data_020dd140[5];

extern const wchar_t native_data_020dd14c[4];

extern const wchar_t native_data_020dd154[4];

extern const wchar_t native_data_020dd15c[5];

extern const wchar_t native_data_020dd168[5];

extern const wchar_t native_data_020dd174[4];

extern const wchar_t native_data_020dd17c[4];
