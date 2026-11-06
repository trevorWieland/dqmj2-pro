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
int native_main_020231e4(const decimal *x, const decimal *y) {
    if (x->sig.text[0] == 0) {
        if (y->sig.text[0] != 0) {
            return 1;
        }

        return 0;
    }

    if (y->sig.text[0] == 0) {
        return 0;
    }

    if (x->exponent == y->exponent) {
        int i;
        int l = x->sig.length;

        if (l > y->sig.length) {
            l = y->sig.length;
        }

        for (i = 0; i < l; ++i) {
            if (x->sig.text[i] < y->sig.text[i]) {
                return 1;
            }

            if (y->sig.text[i] < x->sig.text[i]) {
                return 0;
            }
        }

        if (l == x->sig.length) {
            for (; i < y->sig.length; ++i) {
                if (y->sig.text[i] != 0) {
                    return 1;
                }
            }
        }

        return 0;
    }

    return x->exponent < y->exponent;
}
