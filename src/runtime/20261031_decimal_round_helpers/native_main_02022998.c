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
int native_main_02022998(const decimal *pDecimal, int position) {
    unsigned char const* i = pDecimal->sig.text + position;

    if (*i > 5) {
        return 1;
    }

    if (*i < 5) {
        return -1;
    }

    {
        unsigned char const* e = pDecimal->sig.text + pDecimal->sig.length;

        for (++i; i < e; ++i) {
            if (*i != 0) {
                return 1;
            }
        }
    }

    if (pDecimal->sig.text[position - 1] & 1) {
        return 1;
    }

    return -1;
}
