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
extern u32 native_fn_ov001_021db438();
u32 native_ov001_021dcb44(void) {
    s32 var_r2;
    u32 var_r0;
    u32 var_r4;

    var_r4 = native_fn_ov001_021db438(0, 0);
    var_r0 = native_fn_ov001_021db438(1, 0);
    var_r2 = 0;
    do {
        var_r2 += 1;
        M2C_FIELD(var_r4, u8 *, 0x35C) = (u8) M2C_FIELD(var_r4, u8 *, 0x1FE);
        var_r4 += 0x440;
        M2C_FIELD(var_r0, u8 *, 0x35C) = (u8) M2C_FIELD(var_r0, u8 *, 0x1FE);
        var_r0 += 0x440;
    } while (var_r2 < 3);
    return var_r0;
}
