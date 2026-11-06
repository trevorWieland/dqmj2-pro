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
extern u32 native_fn_02048094();
extern u32 native_fn_02063eec();
u32 native_ov006_021e2a5c(void) {
    u32 var_r0;
    s32 var_r2;
    s32 var_r4;

    var_r0 = native_fn_02063eec();
    var_r4 = 0;
    if (M2C_FIELD(var_r0, u8 *, 1) == 0) {
        return 1U;
    }
    var_r2 = 0;
    do {
        var_r2 += 1;
        if (M2C_FIELD(var_r0, s32 *, 0x34) != 0) {
            var_r4 += 1;
        }
        var_r0 += 0x30;
    } while (var_r2 < 5);
    native_fn_02048094(var_r4, 0);
    native_fn_02048094(5 - var_r4, 0x20);
    return 0U;
}
