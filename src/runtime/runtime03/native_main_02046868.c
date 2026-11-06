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
u32 native_main_02046868(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, u8 arg5) {
    s32 temp_lr;
    s32 temp_r1;
    u32 var_r4;

    temp_lr = (s32) (arg2 - arg0) >> 1;
    var_r4 = 0x10;
    if (arg5 == arg1) {
        if (arg4 == arg0) {
            var_r4 = 0;
        } else if (arg4 == arg2) {
            var_r4 = 2;
        } else {
            var_r4 = 1;
        }
    } else {
        temp_r1 = arg3 - arg5;
        if (temp_r1 == 3) {
            if (arg4 == arg0) {
                var_r4 = 5;
            } else if (arg4 == arg2) {
                var_r4 = 7;
            } else {
                var_r4 = 6;
            }
        } else if (arg5 == arg3) {
            if (arg4 == arg0) {
                var_r4 = 5;
            } else if (arg4 == arg2) {
                var_r4 = 7;
            } else if (arg4 == (temp_lr + 1)) {
                var_r4 = 0xE;
            } else if (arg4 == temp_lr) {
                var_r4 = 0xD;
            } else {
                var_r4 = 6;
            }
        } else if (temp_r1 > 3) {
            if (arg4 == arg0) {
                var_r4 = 3;
            } else if (arg4 == arg2) {
                var_r4 = 4;
            }
        } else if (arg4 == arg0) {
            var_r4 = 3;
        } else if (arg4 == arg2) {
            var_r4 = 4;
        } else if (arg4 == (temp_lr + 1)) {
            var_r4 = 0xC;
        } else if (arg4 == temp_lr) {
            var_r4 = 0xB;
        }
    }
    return var_r4;
}
