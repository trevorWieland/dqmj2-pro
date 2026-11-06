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
extern u32 native_utility_child_arm9_thumb_0200dc5c();
extern u32 native_utility_child_arm9_thumb_0200db84();
extern u32 native_utility_child_arm9_thumb_0200da80();
u32 native_utility_child_arm9_main_0200e1b8(u32 arg0) {
    u32 temp_r0;
    u32 var_r0;

    temp_r0 = native_utility_child_arm9_thumb_0200da80(1, 7);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    native_utility_child_arm9_thumb_0200dc5c(9, arg0);
    var_r0 = native_utility_child_arm9_thumb_0200db84(9, 0);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
