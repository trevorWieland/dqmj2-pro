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
u32 native_main_020349f4(void *arg0, u32 arg1) {
    s32 temp_r0;

    if (arg1 >= (u32) M2C_FIELD(arg0, u16 *, 0)) {
        return 0U;
    }
    temp_r0 = M2C_FIELD(arg0, s32 *, 4);
    if (M2C_FIELD(arg0, u16 *, 2) & 1) {
        return temp_r0 + (arg1 * 0x10);
    }
    return temp_r0 + (arg1 * 8);
}
