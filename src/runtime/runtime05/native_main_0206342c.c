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
extern u32 native_fn_02062a50();
extern u32 native_fn_020633c8();
u32 native_main_0206342c(void) {
    u32 temp_r0;

    temp_r0 = native_fn_02062a50();
    if (temp_r0 == 0) {
        return 0U;
    }
    return native_fn_020633c8(M2C_FIELD(temp_r0, s32 *, 0x14));
}
