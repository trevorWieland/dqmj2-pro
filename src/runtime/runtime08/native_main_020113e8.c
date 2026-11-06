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
extern u32 native_fn_0200a2c4();
extern u32 native_fn_0200a3d0();
extern u32 native_fn_02011414();
extern u8 native_data_020e5d60[];
u32 native_main_020113e8(void) {
    native_fn_0200a2c4();
    native_fn_0200a3d0(0xE, native_fn_02011414);
    M2C_FIELD(native_data_020e5d60, s32 *, 4) = 0;
    return (u32) native_data_020e5d60;
}
