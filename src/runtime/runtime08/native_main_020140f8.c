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
extern u32 native_fn_020072ec();
extern u32 native_fn_02008bf8();
extern u32 native_fn_02011834();
extern u32 native_fn_020118a4();
extern u32 native_fn_02011a34();
extern u8 native_data_020e6820[];
u32 native_main_020140f8(u32 arg0, s32 arg1, u32 arg2, s32 arg3, u16 arg4, u8 arg5) {
    u32 temp_r0;
    u32 var_r0;

    temp_r0 = native_fn_02011a34(2, 7, 9);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    if (arg1 == 0) {
        return 6U;
    }
    if (arg2 > 0x70U) {
        return 6U;
    }
    native_fn_02008bf8(arg1, native_data_020e6820, arg2);
    native_fn_020072ec(native_data_020e6820, arg2);
    native_fn_02011834(0x18, arg0);
    var_r0 = native_fn_020118a4(0x18, 5, native_data_020e6820, arg2, arg3, (s32) arg4, (s32) arg5);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
