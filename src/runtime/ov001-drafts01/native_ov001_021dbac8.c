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
extern u32 native_fn_ov001_021dbaac();
u32 native_ov001_021dbac8(u32 arg0) {
    s32 var_r4;
    u32 var_r5;
    u32 var_r6;

    var_r5 = 0;
    var_r6 = native_fn_ov001_021db438(arg0, 0);
    var_r4 = 0;
loop_1:
    if ((M2C_FIELD(var_r6, u8 *, 0x31C) == 0) || (var_r5 = native_fn_ov001_021dbaac((void *) var_r6), (var_r5 == 0))) {
        var_r4 += 1;
        var_r6 += 0x440;
        if (var_r4 < 3) {
            goto loop_1;
        }
    }
    return var_r5;
}
