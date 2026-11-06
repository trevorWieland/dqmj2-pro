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
u32 native_main_020466f4(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, u8 arg5) {
    u32 var_lr;

    var_lr = 4;
    if (arg5 == arg1) {
        if (arg4 == arg0) {
            var_lr = 0;
        } else if (arg4 == arg2) {
            var_lr = 2;
        } else {
            var_lr = 1;
        }
    } else if (arg5 == arg3) {
        if (arg4 == arg0) {
            var_lr = 6;
        } else if (arg4 == arg2) {
            var_lr = 8;
        } else {
            var_lr = 7;
        }
    } else if (arg4 == arg0) {
        var_lr = 3;
    } else if (arg4 == arg2) {
        var_lr = 5;
    }
    return var_lr;
}
