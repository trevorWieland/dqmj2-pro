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
void native_main_02022b60(decimal *pResult, const decimal *x, const decimal *y) {
    unsigned long accumulator = 0;
    unsigned char mant[64];
    int i = x->sig.length + y->sig.length - 1;
    unsigned char *ip = mant + i + 1;
    unsigned char *ep = ip;
    pResult->sign = 0;

    for (; i > 0; --i) {
        int k = y->sig.length - 1;
        int j = i - k - 1;
        int l;
        int t;
        unsigned char const *jp, *kp;
        
        if (j < 0) {
            j = 0;
            k = i - 1;
        }
        
        jp = x->sig.text + j;
        kp = y->sig.text + k;
        l = k + 1;
        t = x->sig.length - j;
        
        if (l > t) {
            l = t;
        }

        for (; l > 0; --l, ++jp, --kp) {
            accumulator += (unsigned long)(*jp) * *kp;
        }
        
        *--ip = (unsigned char)(accumulator % 10);
        accumulator /= 10;
    }

    pResult->exponent = (short)(x->exponent + y->exponent);

    if (accumulator > 0) {
        *--ip = (unsigned char)accumulator;
        pResult->exponent++;
    }
    
    for (i = 0; i < 32 && ip < ep; ++i, ++ip) {
        pResult->sig.text[i] = *ip;
    }

    pResult->sig.length = i;

    if (ip < ep && *ip >= 5) {
        if (*ip == 5) {
            unsigned char* jp = ip + 1;
            for (; jp < ep; ++jp) {
                if (*jp != 0) {
                    goto round;
                }
            }
        
            if ((*(ip - 1) & 1) == 0) {
                return;
            }
        }
        round:
        
        native_fn_02022a04(pResult, pResult->sig.length);
    }
}
