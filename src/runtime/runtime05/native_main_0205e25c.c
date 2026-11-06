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
extern u32 native_fn_ov000_021da16c();
extern u32 native_fn_ov000_021e683c();
extern u32 native_fn_ov000_021e9dc0();
extern u32 native_fn_ov000_021f3904();
extern u32 native_fn_ov000_02211960();
extern u32 native_fn_ov000_02219e04();
extern u8 native_data_020ddc78[];
u32 native_main_0205e25c(void) {
    if (M2C_FIELD(native_data_020ddc78, u8 *, 1) == 0) {
        return (u32) M2C_FIELD(native_data_020ddc78, u8 *, 1);
    }
    native_fn_ov000_021da16c();
    native_fn_ov000_02211960(1);
    native_fn_ov000_021f3904();
    native_fn_ov000_021e683c();
    native_fn_ov000_02219e04();
    return native_fn_ov000_021e9dc0();
}
