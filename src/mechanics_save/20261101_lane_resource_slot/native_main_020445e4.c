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
#define NULL ((void *)0)
extern u32 native_fn_02008d78(void *, u32, u32);
extern int native_fn_0201d444(u8 *, const u8 *, ...);
extern u32 native_fn_0203cf20(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_0203cf30(u32 arg0, u32 arg1, u32 arg2);
extern u8 native_data_020dd9c0[];
extern u8 native_data_020dd9c8[];
extern u8 native_data_020dd9d4[];

u32 native_main_020445e4(u32 arg0, s32 arg1, void *arg2, s32 arg3) {
    u8 sp20[32];
    u8 sp0[32];
    u32 var_r0;
    u32 var_r4;

    var_r4 = 0;
    native_fn_0201d444(sp20, native_data_020dd9c0, (const u8 *)arg0);
    if (arg1 >= 0) {
        native_fn_0201d444(sp0, native_data_020dd9c8, (const u8 *)arg0, arg1);
    } else {
        native_fn_0201d444(sp0, native_data_020dd9d4, (const u8 *)arg0);
    }
    if (arg3 == 0) {
        var_r0 = native_fn_0203cf20((u32) sp20, (u32) sp0, -1U);
    } else {
        var_r0 = native_fn_0203cf30((u32) sp20, (u32) sp0, -1U);
    }
    if (var_r0 != 0) {
        native_fn_02008d78(arg2, 0U, 0x34U);
        M2C_FIELD(arg2, u32 *, 0x30) = var_r0;
        var_r4 = 1;
    }
    return var_r4;
}
