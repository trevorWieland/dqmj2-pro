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
extern u8 native_data_ov000_0222feb4[];
u32 native_ov000_02225270(s32 arg0) {
    u32 temp_r1;
    u32 var_r0;

    var_r0 = -1U;
    temp_r1 = (u32) (M2C_FIELD((native_data_ov000_0222feb4 + (arg0 * 5)), u8 *, 4) << 0x18) >> 0x1C;
    if (temp_r1 != 1) {
        if (temp_r1 == 2) {
            var_r0 = 0x57;
        }
        return var_r0;
    }
    return 0x52U;
}
