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
extern u32 native_fn_ov001_0220eea4();
extern u8 native_data_ov001_0222f160[];
u32 native_ov001_02210984(void *arg0, u32 arg1, u32 arg2) {
    s32 sp0;
    s32 var_r4;
    u32 var_r2;
    u8 temp_r0;

    var_r2 = arg2;
    if (*native_data_ov001_0222f160 != 0) {
        var_r4 = 0;
loop_2:
        temp_r0 = M2C_FIELD((M2C_FIELD(arg0, s32 *, 0x1E8) + var_r4), u8 *, 0x46);
        if (temp_r0 != 0) {
            if (temp_r0 == 0x30) {
                var_r2 = native_fn_ov001_0220eea4(arg0, arg1, var_r2, &sp0);
                if ((var_r2 == 0) && (sp0 != 0)) {
                    M2C_FIELD(arg0, s32 *, 0x33C) = (s32) (M2C_FIELD(arg0, s32 *, 0x33C) | 1);
                }
            }
            var_r4 += 1;
            if (var_r4 < 0x40) {
                goto loop_2;
            }
        }
    }
    return var_r2;
}
