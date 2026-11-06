typedef unsigned int size_t;

typedef unsigned short wchar_t;

typedef struct decimal {char sign;char pad1;short exp;struct {unsigned char length;unsigned char text[32];unsigned char pad37;} sig;} decimal;

typedef struct decform {char style;char pad1;short digits;} decform;

void native_fn_020236e8(const decform *,double,decimal *);

wchar_t *native_fn_02021274(wchar_t *,const wchar_t *);

size_t native_fn_0201b09c(wchar_t *,const char *,size_t);

extern const unsigned short native_data_020d8f14[128];

static inline int iswupper(wchar_t c){return c>=128?0:native_data_020d8f14[c]&0x200;}

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

void native_main_02020120(decimal *dec, int new_length);

wchar_t* native_main_02020244(long double num, wchar_t *wbuff, print_format format);

void native_main_02020120(decimal *dec, int new_length);

size_t native_fn_0201d69c(const char *);
extern const wchar_t native_data_020dd134[5];
extern const wchar_t native_data_020dd140[5];
extern const wchar_t native_data_020dd14c[4];
extern const wchar_t native_data_020dd154[4];
extern const wchar_t native_data_020dd15c[5];
extern const wchar_t native_data_020dd168[5];
extern const wchar_t native_data_020dd174[4];
extern const wchar_t native_data_020dd17c[4];
