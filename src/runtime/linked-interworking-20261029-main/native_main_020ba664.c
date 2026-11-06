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
extern u32 native_fn_0209bba0();
extern u8 native_data_021d3044[];
u32 native_main_020ba664(u32 arg0) {
    u32 var_r0;
    u32 var_r2;
    u32 temp_r4;

    var_r0 = arg0;
    temp_r4 = var_r0;
    var_r2 = 1;
    if (M2C_FIELD(native_data_021d3044, u32 (**)(), 0x1C) != NULL) {
        var_r0 = M2C_FIELD(native_data_021d3044, u32 (**)(), 0x1C)();
        var_r2 = var_r0;
    }
    if (var_r2 == 0) {
        return var_r0;
    }
    return native_fn_0209bba0(temp_r4);
}
