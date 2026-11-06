typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_ov000_021dfe5c();
extern u32 native_fn_ov000_021dfe80();
extern u32 native_fn_ov000_021dfea4();
u32 native_ov000_021d97e0(void *arg0) {
    s32 var_r4;
    u32 var_r5;
    void *var_r6;

    var_r5 = 0;
    var_r4 = 0;
    var_r6 = arg0;
    do {
        if (M2C_FIELD((arg0 + (var_r4 * 0x10)), u8 *, 0xF) != 0) {
            native_fn_ov000_021dfe5c(var_r4, M2C_FIELD(var_r6, s32 *, 0), M2C_FIELD(var_r6, s32 *, 4), M2C_FIELD(var_r6, s32 *, 8));
            native_fn_ov000_021dfe80(var_r4, M2C_FIELD(var_r6, u8 *, 0xC), M2C_FIELD(var_r6, u8 *, 0xD), M2C_FIELD(var_r6, u8 *, 0xE));
            native_fn_ov000_021dfea4(var_r4, 1);
            var_r5 += 1;
        } else {
            native_fn_ov000_021dfea4(var_r4, 0);
        }
        var_r4 += 1;
        var_r6 += 0x10;
    } while (var_r4 < 4);
    return var_r5;
}
