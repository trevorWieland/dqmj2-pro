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
extern u32 native_utility_child_arm9_thumb_020103f0();
u32 native_utility_child_arm9_main_020103d4(s32 arg0) {
    s32 var_r0;

    var_r0 = arg0;
    if (var_r0 != 1) {
        var_r0 = 0;
    }
    return native_utility_child_arm9_thumb_020103f0(var_r0, 0, 0, 1);
}
