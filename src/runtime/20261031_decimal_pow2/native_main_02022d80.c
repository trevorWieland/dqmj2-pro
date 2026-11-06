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
extern void native_fn_02022ce4(decimal *,const char *,short);
extern void native_fn_02022b60(decimal *,const decimal *,const decimal *);
extern const char native_data_020dd1cc[];
extern const char native_data_020dd1fc[];
extern const char native_data_020dd224[];
extern const char native_data_020dd23c[];
extern const char native_data_020dd24c[];
extern const char native_data_020dd254[];
extern const char native_data_020dd25c[];
extern const char native_data_020dd264[];
extern const char native_data_020dd26c[];
extern const char native_data_020dd270[];
extern const char native_data_020dd274[];
extern const char native_data_020dd278[];
extern const char native_data_020dd27c[];
extern const char native_data_020dd280[];
extern const char native_data_020dd284[];
extern const char native_data_020dd288[];
extern const char native_data_020dd28c[];
extern const char native_data_020dd290[];
extern const char native_data_020dd294[];
extern const char native_data_020dd298[];
extern const char native_data_020dd29c[];
void native_main_02022d80(decimal *pDecimal, long exp) {
    switch (exp) {
        case -64:
            native_fn_02022ce4(pDecimal, native_data_020dd1cc, -20);
            return;
        case -53:
            native_fn_02022ce4(pDecimal, native_data_020dd1fc, -16);
            return;
        case -32:
            native_fn_02022ce4(pDecimal, native_data_020dd224, -10);
            return;
        case -16:
            native_fn_02022ce4(pDecimal, native_data_020dd23c, -5);
            return;
        case -8:
            native_fn_02022ce4(pDecimal, native_data_020dd24c, -3);
            return;
        case -7:
            native_fn_02022ce4(pDecimal, native_data_020dd254, -3);
            return;
        case -6:
            native_fn_02022ce4(pDecimal, native_data_020dd25c, -2);
            return;
        case -5:
            native_fn_02022ce4(pDecimal, native_data_020dd264, -2);
            return;
        case -4:
            native_fn_02022ce4(pDecimal, native_data_020dd26c, -2);
            return;
        case -3:
            native_fn_02022ce4(pDecimal, native_data_020dd270, -1);
            return;
        case -2:
            native_fn_02022ce4(pDecimal, native_data_020dd274, -1);
            return;
        case -1:
            native_fn_02022ce4(pDecimal, native_data_020dd278, -1);
            return;
        case 0:
            native_fn_02022ce4(pDecimal, native_data_020dd27c, 0);
            return;
        case 1:
            native_fn_02022ce4(pDecimal, native_data_020dd280, 0);
            return;
        case 2:
            native_fn_02022ce4(pDecimal, native_data_020dd284, 0);
            return;
        case 3:
            native_fn_02022ce4(pDecimal, native_data_020dd288, 0);
            return;
        case 4:
            native_fn_02022ce4(pDecimal, native_data_020dd28c, 1);
            return;
        case 5:
            native_fn_02022ce4(pDecimal, native_data_020dd290, 1);
            return;
        case 6:
            native_fn_02022ce4(pDecimal, native_data_020dd294, 1);
            return;
        case 7:
            native_fn_02022ce4(pDecimal, native_data_020dd298, 2);
            return;
        case 8:
            native_fn_02022ce4(pDecimal, native_data_020dd29c, 2);
            return;
    }

    {
        decimal dec, temp;
        native_main_02022d80(&dec, ((long)((0x80000000UL & exp) >> 31) + exp) >> 1);
        native_fn_02022b60(pDecimal, &dec, &dec);

        if (exp & 0x1) {
            temp = *pDecimal;

            if (exp > 0) {
                native_fn_02022ce4(&dec, native_data_020dd280, 0);
            }
            else {
                native_fn_02022ce4(&dec, native_data_020dd278, -1);
            }

            native_fn_02022b60(pDecimal, &temp, &dec);
        }
    }
}
