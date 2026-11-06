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
extern u32 native_fn_0205f13c();
extern u32 native_fn_0205f838();
extern u8 native_data_021079d8[];
u32 native_main_0205e7a8(u32 arg0, u32 arg1) {
    s32 temp_r0;

    temp_r0 = (s32) native_fn_0205f13c(arg0, arg1, -1, -1);
    if (temp_r0 < 0) {
        goto block_2;
    }
    native_fn_02008d78(native_data_021079d8 + (temp_r0 * 0x10), 0, 0x10);
block_2:
    native_fn_0205f838();
    return (u32) temp_r0;
}
