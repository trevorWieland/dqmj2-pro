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
extern u32 native_fn_02008e0c();
extern u8 native_data_021cebe0[];
extern u8 native_data_021cec64[];
u32 native_itcm_01ffb810(s32 arg0, s32 arg1, s16 arg2) {
    M2C_FIELD(native_data_021cebe0, s16 *, 0x82) = arg2;
    M2C_FIELD(native_data_021cebe0, s16 *, 0x80) = 0;
    native_fn_02008e0c(arg0, native_data_021cec64, arg1);
    M2C_FIELD(native_data_021cebe0, s8 *, 3) = 1;
    return (u32) native_data_021cebe0;
}
