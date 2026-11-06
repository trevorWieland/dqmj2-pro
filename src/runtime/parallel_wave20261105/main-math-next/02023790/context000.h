typedef unsigned char u8;

typedef struct decimal {
    char sign;
    char pad0;
    short exponent;
    struct { u8 length; u8 text[32]; u8 pad; } sig;
} decimal;

extern const float native_data_020dceb8;

extern double native_fn_02025930(float);

extern const double native_data_020dd18c[8];

extern const char native_data_020dd2a0[37];

extern double native_fn_0202263c(double,double);

extern double native_fn_0202298c(double,double);

extern double native_fn_02022740(double,int);

extern int native_fn_02023e5c(double);

extern void native_fn_02022ce4(decimal*,const char*,short);

extern int native_fn_020231e4(const decimal*,const decimal*);

extern int native_fn_02023104(const decimal*,const decimal*);

extern void native_fn_020232c4(decimal*,const decimal*,const decimal*);

extern void native_fn_02023568(decimal*,double);
