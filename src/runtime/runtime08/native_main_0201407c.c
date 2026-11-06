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
extern u32 native_fn_02011834();
extern u32 native_fn_020118a4();
extern u32 native_fn_020119ec();
u32 native_main_0201407c(u32 arg0, u32 arg1, s32 arg2, s32 arg3) {
    u32 temp_r0;
    u32 var_r0;

    temp_r0 = native_fn_020119ec();
    if (temp_r0 != 0) {
        return temp_r0;
    }
    if (arg1 > 3U) {
        return 6U;
    }
    if (arg1 != 0) {
        if (arg3 == 0) {
            return 6U;
        }
        native_fn_020072ec(arg3, 0x50);
        goto block_8;
    }
block_8:
    native_fn_02011834(0x27, arg0);
    var_r0 = native_fn_020118a4(0x27, 3, arg1, arg3, arg2);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
