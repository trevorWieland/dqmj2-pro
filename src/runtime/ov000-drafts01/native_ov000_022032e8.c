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
extern u32 native_fn_02061c1c();
extern u32 native_fn_ov000_02214a38();
typedef struct {
    u8 unknown_0[0x4];
    s8 field_4;
    s8 field_5;
    u8 unknown_6[0x5];
    s8 field_b;
} Record_native_data_ov000_02238190;
extern Record_native_data_ov000_02238190 native_data_ov000_02238190;
u32 native_ov000_022032e8(void) {
    if (native_data_ov000_02238190.field_b != 0) {
        return (u32) native_data_ov000_02238190.field_b;
    }
    native_fn_02061c1c(0, 3, 2, 0x11, 2, 0, 1);
    native_fn_02061c1c(2, 0x14, 2, 8, 2, 0, 1);
    native_fn_02061c1c(3, 3, 5, 0x1A, 2, 0, 1);
    native_data_ov000_02238190.field_b = 1;
    native_data_ov000_02238190.field_4 = 0;
    native_data_ov000_02238190.field_5 = 0;
    return native_fn_ov000_02214a38(0, 0);
}
