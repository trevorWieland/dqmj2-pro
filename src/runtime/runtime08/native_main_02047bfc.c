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
extern u32 native_fn_02008c14();
extern u32 native_fn_02021258();
extern u32 native_fn_02021294();
extern u32 native_fn_02047c68();
extern u8 native_data_020facdc[];
extern u8 native_data_020fb264[];
u32 native_main_02047bfc(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;

    native_fn_02008c14(0, native_data_020facdc, 0x80);
    temp_r0 = native_fn_02047c68(arg1, arg2, arg3);
    native_fn_02021294(arg0, temp_r0);
    M2C_FIELD(native_data_020fb264, u16 *, 0x80) = (u16) (M2C_FIELD(native_data_020fb264, u16 *, 0x80) + native_fn_02021258(temp_r0));
    return 0U;
}
