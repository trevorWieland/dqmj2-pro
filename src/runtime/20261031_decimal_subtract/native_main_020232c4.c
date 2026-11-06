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
void native_main_020232c4(decimal *z, const decimal *x, const decimal *y) {
    int zlen, dexp;
    unsigned char *ib, *i, *ie;
    unsigned char const *jb, *j, *jn;
    *z = *x;

    if (y->sig.text[0] == 0) {
        return;
    }

    zlen = z->sig.length;

    if (zlen < y->sig.length) {
        zlen = y->sig.length;
    }

    dexp = z->exponent - y->exponent;
    zlen += dexp;

    if (zlen > 32) {
        zlen = 32;
    }
 
    while (z->sig.length < zlen) {
        z->sig.text[z->sig.length++] = 0;
    }

    ib = z->sig.text;
    i = ib + zlen;

    if (y->sig.length + dexp < zlen) {
        i = ib + (y->sig.length + dexp);
    }

    jb = y->sig.text;
    j = jb + (i - ib - dexp);
    jn = j;

    while (i > ib && j > jb) {
        --i;
        --j;
        if (*i < *j) {
            unsigned char *k = i - 1;
            while (*k == 0) {
                --k;
            }
            while (k != i) {
                --*k;
                *++k += 10;
            }
        }

        *i -= *j;
    }

    if (jn - jb < y->sig.length) {
        BOOL round_down = FALSE; 
        if (*jn < 5) {
            round_down = TRUE;
        }
        else if (*jn == 5) {
            unsigned char const *je = y->sig.text + y->sig.length;
    
            for (j = jn + 1; j < je; ++j) {
                if (*j != 0) {
                    goto done;
                }
            }

            i = ib + (jn - jb) + dexp - 1;

            if (*i & 1) {
                round_down = 1;
            }
        }
        if (round_down) {
            if (*i < 1) {
                unsigned char *k = i - 1;

                while (*k == 0) {
                    --k;
                }
                while (k != i) {
                    --*k;
                    *++k += 10;
                }
            }

            *i -= 1;
        }
    }

done:
    for (i = ib; *i == 0; ++i);

    if (i > ib) {
        unsigned char dl = (unsigned char)(i - ib);
        z->exponent -= dl;
        ie = ib + z->sig.length;
        for (; i < ie; ++i, ++ib)
            *ib = *i;
        z->sig.length -= dl;
    }

    ib = z->sig.text;

    for (i = ib + z->sig.length; i > ib;) {
        --i;
        if (*i != 0) {
            break;
        }
    }

    z->sig.length = (unsigned char)(i - ib + 1);
}
