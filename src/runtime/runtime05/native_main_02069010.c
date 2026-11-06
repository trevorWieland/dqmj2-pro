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
extern u32 native_fn_02045dc4();
extern u8 native_data_021c492c[];
u32 native_main_02069010(s32 arg0) {
    s32 temp_r4;
    u8 temp_r0;

    temp_r4 = (arg0 * 0x14) + (s32) native_data_021c492c;
    temp_r0 = M2C_FIELD(temp_r4, u8 *, 0x11);
    if (temp_r0 == 0) {
        return (u32) temp_r0;
    }
    native_fn_02045dc4(M2C_FIELD(temp_r4, u8 *, 0xE), M2C_FIELD(temp_r4, u8 *, 0xF), M2C_FIELD(temp_r4, u8 *, 0xC), M2C_FIELD(temp_r4, u8 *, 0xD), 2, 2);
    M2C_FIELD(temp_r4, u8 *, 0x11) = 0U;
    return 0U;
}
