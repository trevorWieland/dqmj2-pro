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
extern u32 native_fn_0209477c();
extern u32 native_fn_0209529c();
u32 native_main_02094420(void) {
    u32 temp_r0;

    temp_r0 = native_fn_0209477c();
    if (temp_r0 <= 1U) {
        return 0U;
    }
    if (temp_r0 < 7U) {
        return 1U;
    }
    if (temp_r0 == 9) {
        return 4U;
    }
    if (temp_r0 < 0xAU) {
        return 2U;
    }
    if (temp_r0 == 0xB) {
        return 4U;
    }
    if (temp_r0 < 0x10U) {
        return 3U;
    }
    if (temp_r0 == 0x10) {
        return 5U;
    }
    if (temp_r0 == 0x11) {
        return 4U;
    }
    return native_fn_0209529c();
}
