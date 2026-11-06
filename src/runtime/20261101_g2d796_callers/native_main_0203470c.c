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
extern u32 native_fn_02034480(u32 rawHeader, u32 signature);
extern u32 native_fn_02034748(u32 rawData);
u32 native_main_0203470c(u32 arg0, s32 *arg1) {
    u32 temp_r0;

    temp_r0 = native_fn_02034480(arg0, 0x504C5454);
    if (temp_r0 == 0) {
        *arg1 = 0;
        return 0U;
    }
    native_fn_02034748(temp_r0 + 8);
    *arg1 = temp_r0 + 8;
    return 1U;
}
