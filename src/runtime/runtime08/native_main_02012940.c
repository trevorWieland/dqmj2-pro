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
u32 native_main_02012940(void *arg0) {
    u16 temp_r0;
    u16 temp_r1;

    if ((u32) M2C_FIELD(arg0, u16 *, 4) > 0x70U) {
        return 0U;
    }
    temp_r1 = M2C_FIELD(arg0, u16 *, 0x18);
    if (((u32) temp_r1 < 0xAU) || ((u32) temp_r1 > 0x3E8U)) {
        return 0U;
    }
    temp_r0 = M2C_FIELD(arg0, u16 *, 0x32);
    if (((u32) temp_r0 < 1U) || ((u32) temp_r0 > 0xEU)) {
        return 0U;
    }
    return 1U;
}
