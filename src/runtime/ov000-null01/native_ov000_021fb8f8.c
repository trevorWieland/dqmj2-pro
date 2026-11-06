#define NULL ((void *)0)
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
extern u32 native_fn_ov000_021fb9a8();
extern u32 native_fn_ov000_021fbad8();
extern u8 native_data_ov000_02237170[];
u32 native_ov000_021fb8f8(u32 arg0, u8 *arg1) {
    s32 temp_r0;
    s16 temp_r1;
    u8 var_r4;
    u8 var_r5;
    s32 var_r6;
    s32 temp_r7;
    u8 *var_r8;

    var_r8 = arg1;
    var_r5 = 0xFF;
    var_r6 = 0;
    if (var_r8 == NULL) {
        native_fn_ov000_021fbad8(native_data_ov000_02237170, 1);
        var_r8 = native_data_ov000_02237170;
    }
    var_r4 = 0;
    do {
        temp_r7 = (var_r4 * 0x34) + (s32) var_r8;
        temp_r1 = M2C_FIELD(native_fn_ov000_021fb9a8(temp_r7, arg0), s16 *, 2);
        if ((temp_r1 != 0) && (M2C_FIELD(temp_r7, u8 *, 0) != 0)) {
            temp_r0 = M2C_FIELD(temp_r7, s32 *, 0xC) - temp_r1;
            if (var_r6 <= temp_r0) {
                var_r5 = var_r4;
                var_r6 = temp_r0;
            }
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 6U);
    return (u32) var_r5;
}
