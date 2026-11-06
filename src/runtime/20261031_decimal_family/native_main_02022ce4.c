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
extern void native_fn_02022a04(decimal *, int);
void native_main_02022ce4(decimal *pDecimal, const char *pStr, short exp) {
    int i;
    pDecimal->exponent = exp;
    pDecimal->sign = 0;

    for (i = 0; i < 32 && *pStr != 0;) {
        pDecimal->sig.text[i++] = (unsigned char)(*pStr++ - '0');
    }

    pDecimal->sig.length = i;

    if (*pStr != 0) {
        if (*pStr < 5) {
            return;
        }

        if (*pStr > 5) {
            goto round;
        }

        {
            const char* p = pStr + 1;
            for (; *p != 0; ++p) {
                if (*p != '0') {
                    goto round;
                }
            }

            if ((pDecimal->sig.text[i - 1] & 1) == 0) {
                return;
            }
        }

        round:
            native_fn_02022a04(pDecimal, pDecimal->sig.length);
    }
}
