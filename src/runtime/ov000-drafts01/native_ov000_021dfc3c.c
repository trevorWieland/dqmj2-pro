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
extern u32 native_fn_ov000_021df5a8();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov000_02231bf0;
extern Record_native_data_ov000_02231bf0 native_data_ov000_02231bf0;
u32 native_ov000_021dfc3c(s32 arg0, s32 arg1) {
    if (native_data_ov000_02231bf0.field_8 != 0) {
        return (u32) M2C_FIELD(((arg0 * 0x2C) + native_data_ov000_02231bf0.field_8 + (arg1 * 2)), u16 *, 0x18);
    }
    return (u32) M2C_FIELD((native_fn_ov000_021df5a8() + (arg1 * 2)), u16 *, 0x18);
}
