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
extern u8 native_data_020ddb80[];
extern u8 native_data_02102e2c[];
extern u8 native_data_021043ac[];
u32 native_main_0205c3c4(void) {
    native_fn_02008d78(native_data_02102e2c, 0, 0x1580);
    native_fn_02008d78(native_data_021043ac, 0, 0x2380);
    *native_data_020ddb80 = 1;
    return (u32) native_data_020ddb80;
}
