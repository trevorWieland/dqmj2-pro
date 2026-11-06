typedef unsigned char u8;

typedef struct decimal {
    char sign;
    char pad0;
    short exponent;
    struct { u8 length; u8 text[32]; u8 pad; } sig;
} decimal;

extern unsigned long long native_fn_020260dc(unsigned long long,unsigned long long);

extern unsigned long long native_fn_020260e8(unsigned long long,unsigned long long);
