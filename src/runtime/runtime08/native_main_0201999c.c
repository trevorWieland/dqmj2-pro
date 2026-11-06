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
u32 native_main_0201999c(u32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r1;

    temp_r0_2 = arg0 - (0x55555555 & (arg0 >> 1));
    temp_r1 = (temp_r0_2 & 0x33333333) + (0x33333333 & (temp_r0_2 >> 2));
    temp_r0_3 = (temp_r1 + (temp_r1 >> 4)) & 0x0F0F0F0F;
    temp_r0 = temp_r0_3 + (temp_r0_3 >> 8);
    return (u32) (u8) (temp_r0 + (temp_r0 >> 0x10));
}
