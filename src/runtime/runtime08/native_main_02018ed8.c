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
extern u8 native_data_020ec3a4[];
u32 native_main_02018ed8(u32 arg0) {
    s32 temp_r4;
    void *temp_r0;

    if (M2C_FIELD(native_data_020ec3a4, s32 *, 4) == 0) {
        return arg0;
    }
    temp_r4 = arg0 - 1;
    native_fn_02008d78(M2C_FIELD(native_data_020ec3a4, s32 *, 4) + (temp_r4 << 5), 0, 0x1E);
    temp_r0 = M2C_FIELD(native_data_020ec3a4, s32 *, 4) + (temp_r4 * 4);
    M2C_FIELD(temp_r0, s32 *, 0x1E0) = 0;
    return (u32) temp_r0;
}
