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
extern u32 native_fn_0205dbf0();
extern u32 native_fn_0205f5f4();
extern u32 native_fn_020c41f0();
extern u8 native_data_020daef8[];
extern u8 native_data_020daf0c[];
extern u8 native_data_021d5398[];
extern u8 native_data_021d53b0[];
u32 native_main_020c3df4(void) {
    native_fn_020c41f0();
    native_fn_0205f5f4(M2C_FIELD(native_data_021d5398, s32 *, 0x14));
    return native_fn_0205dbf0(2, native_data_021d53b0, native_data_020daf0c, native_data_020daef8, 9);
}
