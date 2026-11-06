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
extern u32 native_fn_0202a498();
extern u8 native_data_021cebe0[];
u32 native_itcm_01ffa22c(void) {
    native_fn_0202a498(8, M2C_FIELD(native_data_021cebe0, s32 *, 0x18));
    native_fn_0202a498(8, M2C_FIELD(native_data_021cebe0, s32 *, 0x14));
    native_fn_0202a498(8, M2C_FIELD(native_data_021cebe0, s32 *, 0x34));
    native_fn_0202a498(8, M2C_FIELD(native_data_021cebe0, s32 *, 0x2C));
    native_fn_0202a498(8, M2C_FIELD(native_data_021cebe0, s32 *, 0x10));
    M2C_FIELD(native_data_021cebe0, s32 *, 0x18) = 0;
    M2C_FIELD(native_data_021cebe0, s32 *, 0x14) = 0;
    M2C_FIELD(native_data_021cebe0, s32 *, 0x34) = 0;
    M2C_FIELD(native_data_021cebe0, s32 *, 0x2C) = 0;
    M2C_FIELD(native_data_021cebe0, s32 *, 0x10) = 0;
    return (u32) native_data_021cebe0;
}
