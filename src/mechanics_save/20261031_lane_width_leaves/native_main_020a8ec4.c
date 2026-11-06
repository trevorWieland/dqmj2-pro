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
extern u8 native_data_020d8d04[] __attribute__((aligned(2)));
u32 native_main_020a8ec4(s8 *arg0) {
    s8 *var_r0;
    s8 *temp_r3;
    s32 var_r4;

    var_r0 = arg0;
    var_r4 = *var_r0;
    temp_r3 = var_r0;
    if (var_r4 != 0) {
        do {
            if (((s32) var_r4 >= 0) && ((s32) var_r4 < 0x80)) {
                var_r4 = (u8) native_data_020d8d04[var_r4];
            }
            *var_r0 = var_r4;
            var_r0 += 1;
            var_r4 = *var_r0;
        } while (var_r4 != 0);
    }
    return (u32) temp_r3;
}
