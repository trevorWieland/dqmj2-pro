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
extern u32 native_fn_02008d78();
extern u32 native_fn_020631d4();
extern u32 native_fn_020bae1c();
extern u8 native_data_021b9eb4[];
extern u8 native_data_021b9ee8[];
extern u8 native_data_021bb278[];
extern u8 native_data_021bd51c[];
u32 native_main_020625cc(void) {
    native_fn_02008d78(native_data_021bd51c, 0, 0x39D8);
    native_fn_02008d78(native_data_021b9eb4, 0, 0x34);
    native_fn_02008d78(native_data_021bb278, 0, 0x22A4);
    native_fn_02008d78(native_data_021b9ee8, 0, 0x1390);
    native_fn_020631d4();
    return native_fn_020bae1c();
}
