#define NULL ((void *)0)
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
extern u8 native_data_020f5bf0[];
extern u8 native_data_020f5c00[];
u32 native_main_0203c578(u8 *arg0, s32 arg1, s32 arg2, s8 arg3) {
    u8 *var_r0;

    var_r0 = arg0;
    if (var_r0 == NULL) {
        var_r0 = native_data_020f5c00;
    }
    M2C_FIELD(var_r0, s32 *, 0) = arg1;
    M2C_FIELD(var_r0, s32 *, 4) = arg2;
    M2C_FIELD(var_r0, s8 *, 8) = arg3;
    M2C_FIELD(var_r0, s32 *, 0xC) = -0x1F4000;
    M2C_FIELD(var_r0, s32 *, 0x10) = 0x1F4000;
    *native_data_020f5bf0 = 0;
    return 1U;
}
