typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u8 sign;
    u8 reserved;
    s16 exponent;
    u8 count;
    u8 digits[];
} Decimal;
extern void native_fn_02023568(Decimal *, u32, u32);
extern void native_fn_02022a54(void *, s32);
u32 native_main_020236e8(const Decimal *settings, u32 low, u32 high, Decimal *out) {
    s16 limit = settings->exponent;
    s32 index;
    native_fn_02023568(out, low, high);
    if (out->digits[0] > 9) return out->digits[0];
    if (limit > 32) limit = 32;
    native_fn_02022a54(out, limit);
    while (out->count < limit) {
        u32 previous = out->count;
        out->count++;
        out->digits[previous] = 0;
    }
    out->exponent -= out->count - 1;
    for (index = 0; index < out->count; index++) out->digits[index] += 48;
    return out->count;
}
