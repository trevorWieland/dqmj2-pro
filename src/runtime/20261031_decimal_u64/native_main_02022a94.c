typedef unsigned char u8;
typedef unsigned int u32;
typedef int BOOL;
#define FALSE 0
#define TRUE 1
typedef struct decimal {
    char sign;
    char pad0;
    short exponent;
    struct { u8 length; u8 text[32]; u8 pad; } sig;
} decimal;
extern unsigned long long native_fn_020260dc(unsigned long long,unsigned long long);
extern unsigned long long native_fn_020260e8(unsigned long long,unsigned long long);
void native_main_02022a94(decimal *pDecimal, unsigned long long input) {
    pDecimal->sign = 0;
    pDecimal->sig.length = 0;

    for (; input != 0; input = native_fn_020260dc(input, 10)) {
        pDecimal->sig.text[pDecimal->sig.length++] = (unsigned char)(native_fn_020260e8(input, 10));
    }

    
    {
        unsigned char* start = pDecimal->sig.text;
        unsigned char* end = pDecimal->sig.text + pDecimal->sig.length;

        for (; start < --end; ++start) {
            unsigned char t = *start;
            *start = *end;
            *end = t;
        }
    }

    pDecimal->exponent = (short)(pDecimal->sig.length - 1);
}
