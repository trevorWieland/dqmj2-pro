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
extern int native_fn_02023e48(double);
extern int native_fn_02023e5c(double);
extern double native_fn_02022684(double,int*);
extern int native_fn_02023db4(unsigned long long);
extern void native_fn_02022d80(decimal*,long);
extern void native_fn_02022a94(decimal*,unsigned long long);
extern double native_fn_02022740(double,int);
extern void native_fn_02022b60(decimal*,const decimal*,const decimal*);
static inline int decimal_trailing(double x) {
    unsigned long long bits = *(unsigned long long *)&x | 0x0010000000000000ULL;
    return native_fn_02023db4((bits & -bits) - 1);
}
void native_main_02023568(decimal *pDecimal, double x) {
	char sign = (char)(native_fn_02023e48(x) != 0);
	if (x == 0.0) {
		pDecimal->sign = sign;
		pDecimal->exponent = 0;
		pDecimal->sig.length = 1;
		pDecimal->sig.text[0] = 0;
		return;
	}

	if (!(native_fn_02023e5c(x) > 2)) {
		pDecimal->sign = sign;
		pDecimal->exponent = 0;
		pDecimal->sig.length = 1;
		pDecimal->sig.text[0] = (unsigned char)(native_fn_02023e5c(x) == 1 ? 'N' : 'I');
		return;
	}

	if (sign) {
		x = -x;
    }

	{
        int exp;
        double frac = native_fn_02022684(x, &exp);
        long num_bits_extract = 53 - decimal_trailing(frac);
        decimal int_d, pow2_d;
        native_fn_02022d80(&pow2_d, exp-num_bits_extract);
        native_fn_02022a94(&int_d, (unsigned long long)native_fn_02022740(frac, (int)num_bits_extract));
        native_fn_02022b60(pDecimal, &int_d, &pow2_d);
        pDecimal->sign = sign;
	}
}
