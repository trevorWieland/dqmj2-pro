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
extern u32 native_fn_020443ec();
extern u32 native_fn_0204458c();
u32 native_ov001_021d9960(s32 arg0, s32 arg1) {
    u32 temp_r0;
    u32 temp_r4;
    u32 var_r0;

    temp_r4 = native_fn_020443ec();
    temp_r0 = native_fn_0204458c();
    if (arg0 == 1) {
        if (arg1 == 0x63) {
            return 2U;
        }
        if (temp_r4 == 0) {
            return 1U;
        }
        else if (temp_r4 == 8) {
            return 1U;
        }
        else if (temp_r4 == 1) {
            return 3U;
        }
        else if (temp_r4 == 4) {
            return 0U;
        }
        else if (temp_r4 == 3) {
            return 0U;
        }
        else if (temp_r4 == 5) {
            return 0U;
        }
        else if (temp_r4 == 7) {
            return 0U;
        }
        else if (temp_r4 == 6) {
            return 0U;
        }
        else {
            if (temp_r0 == 0) {
                var_r0 = 1;
            } else {
                var_r0 = 0;
            }
            return var_r0;
        }

    } else {
        return 0U;
    }
}
