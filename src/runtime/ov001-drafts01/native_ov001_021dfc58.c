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
extern u32 native_fn_ov001_021dfb30();
typedef struct {
    u8 unknown_0[0x10];
    u8 field_10;
    u8 unknown_11[0x13];
    u8 field_24;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021dfc58(s32 arg0, s8 *arg1, u32 arg2, s8 arg3, s32 arg4) {
    s8 temp_r0;
    s8 temp_r0_2;

    if (arg0 & (native_data_ov001_022388ec.field_10 & ~native_data_ov001_022388ec.field_24)) {
        *arg1 = arg3;
        native_fn_ov001_021dfb30(arg4, arg2, arg3, 1);
    }
    temp_r0_2 = *arg1;
    if ((s32) temp_r0_2 <= 0) {
        return (u32) temp_r0_2;
    }
    *arg1 = temp_r0_2 - 1;
    temp_r0 = *arg1;
    if ((s32) temp_r0 > 0) {
        return (u32) temp_r0;
    }
    native_data_ov001_022388ec.field_10 = (u8) (native_data_ov001_022388ec.field_10 & ~arg0);
    return native_fn_ov001_021dfb30(arg4, arg2, 0, 0);
}
