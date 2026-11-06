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
extern u32 native_fn_ov000_020c013c();
extern u32 native_fn_ov000_020c0210();
extern u32 native_fn_ov000_020693e0();
extern u32 native_fn_ov000_02068d54();
extern u8 native_data_ov000_02101ae8[];
u32 native_ov000_0221da3c(void) {
    native_fn_ov000_020c0210();
    native_fn_ov000_020c013c();
    native_fn_ov000_02068d54();
    native_fn_ov000_020693e0();
    M2C_FIELD(native_data_ov000_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_ov000_02101ae8;
}
