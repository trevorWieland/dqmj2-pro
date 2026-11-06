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
void native_main_02022a04(decimal *pDecimal, int digits) {
    unsigned char *b = pDecimal->sig.text;
    unsigned char *i = b + digits - 1;

    while (1) {
        if (*i < 9) {
            (*i)++;
            return;
        }

        if (i == b) {
            *i = 1;
            pDecimal->exponent++;
            return;
        }
        
        *i-- = 0;
    }
}
