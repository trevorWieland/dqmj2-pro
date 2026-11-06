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
extern u32 native_fn_02086ba8();
u32 native_main_02086b68(u32 arg0, s32 arg1, s32 arg2) {
    s32 var_r5;
    u32 temp_r0;

    var_r5 = 0;
    if (arg2 <= 0) {
        return arg0;
    }
    do {
        temp_r0 = native_fn_02086ba8(arg0, arg1 + (var_r5 * 2), 0);
        var_r5 += temp_r0;
    } while (var_r5 < arg2);
    return temp_r0;
}
