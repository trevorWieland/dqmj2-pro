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
u32 native_main_02046964(u32 arg0, s32 arg1, s32 arg2, s32 arg3, u32 arg4, u8 arg5, u8 arg6) {
    s32 temp_r0;
    s32 temp_r0_2;
    s32 temp_r0_3;
    u32 var_r6;
    u8 temp_r4;

    temp_r4 = arg6 + 1;
    var_r6 = 4;
    if (arg5 == arg1) {
        if (arg4 <= arg0) {
            var_r6 = 0x13;
        } else if (arg4 == (arg0 + 1)) {
            var_r6 = 9;
        } else {
            temp_r0 = arg4 - arg0;
            if (temp_r0 > (s32) temp_r4) {
                var_r6 = 0x13;
            } else if (temp_r4 == temp_r0) {
                var_r6 = 0xB;
            } else {
                var_r6 = 0xA;
            }
        }
    } else if (arg5 == (arg1 + 1)) {
        if (arg4 == arg0) {
            var_r6 = 0;
        } else if (arg4 == arg2) {
            var_r6 = 2;
        } else if (arg4 <= arg0) {
            var_r6 = 1;
        } else if (arg4 == (arg0 + 1)) {
            var_r6 = 0xC;
        } else {
            temp_r0_2 = arg4 - arg0;
            if (temp_r0_2 > (s32) temp_r4) {
                var_r6 = 1;
            } else if (temp_r4 == temp_r0_2) {
                var_r6 = 0xE;
            } else {
                var_r6 = 0xD;
            }
        }
    } else if (arg5 == (arg1 + 2)) {
        if (arg4 == arg0) {
            var_r6 = 3;
        } else if (arg4 == arg2) {
            var_r6 = 5;
        } else if (arg4 == (arg0 + 1)) {
            var_r6 = 0xF;
        } else {
            temp_r0_3 = arg4 - arg0;
            if (temp_r0_3 <= (s32) temp_r4) {
                if (temp_r4 == temp_r0_3) {
                    var_r6 = 0x11;
                } else {
                    var_r6 = 0x10;
                }
            }
        }
    } else if (arg5 == arg3) {
        if (arg4 == arg0) {
            var_r6 = 6;
        } else if (arg4 == arg2) {
            var_r6 = 8;
        } else {
            var_r6 = 7;
        }
    } else if (arg4 == arg0) {
        var_r6 = 3;
    } else if (arg4 == arg2) {
        var_r6 = 5;
    }
    return var_r6;
}
