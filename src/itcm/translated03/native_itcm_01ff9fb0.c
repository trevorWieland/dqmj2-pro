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
extern u32 native_fn_02008d78();
extern u8 native_data_021cebe0[];
extern u8 native_data_021cec60[];
extern u8 native_data_021ceca0[];
u32 native_itcm_01ff9fb0(void) {
    native_fn_02008d78(native_data_021cec60, 0, 0x3C);
    native_fn_02008d78(native_data_021ceca0, 0, 0x54);
    M2C_FIELD(native_data_021cebe0, s32 *, 0x30) = 1;
    M2C_FIELD(native_data_021cebe0, s8 *, 3) = 0;
    M2C_FIELD(native_data_021cebe0, s32 *, 0x1C) = 0;
    return (u32) native_data_021cebe0;
}
