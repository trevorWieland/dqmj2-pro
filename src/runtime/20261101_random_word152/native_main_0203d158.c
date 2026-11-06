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
#define NULL ((void *)0)
extern u32 native_fn_0203d1f0();
extern u32 native_fn_0203d294();
typedef struct {
    u8 unknown_0[0xc];
    u32 field_c;
} Record_native_data_020f6028;
extern Record_native_data_020f6028 native_data_020f6028;
u32 native_main_0203d158(u32 arg0) {
    u16 high_half;
    u8 temp_r0;
    u8 temp_r4;
    u32 temp_r5;

    if (arg0 != 0) {
        temp_r4 = (u8) native_fn_0203d294(0x100U);
        temp_r0 = (u8) native_fn_0203d294(0x100U);
        high_half = (u16) ((temp_r4 * ~temp_r0) + 0x7B);
        native_data_020f6028.field_c = (temp_r4 | (temp_r0 << 8)) | ((u32) high_half << 16);
    } else {
        do {
            temp_r5 = native_fn_0203d294(0xFFFFU);
            native_data_020f6028.field_c = (u32) ((temp_r5 + 1) * (native_fn_0203d294(0xFFFFU) + 1));
        } while (native_fn_0203d1f0() != 0);
    }
    return native_data_020f6028.field_c;
}
