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
extern u32 native_fn_020a8640();
extern u32 native_fn_020b3d04();
extern u32 native_fn_020b3e80();
u32 native_main_020b46f8(void *arg0, u32 arg1, u32 arg2) {
    s32 temp_r0;

    temp_r0 = M2C_FIELD(arg0, s32 *, 0xC);
    if ((temp_r0 != 5) && (temp_r0 != 6)) {
        return 1U;
    }
    if (native_fn_020a8640(M2C_FIELD(arg0, s32 *, 0x9C)) != 0) {
        if (native_fn_020b3e80(arg0, 0, arg1, arg2, 0) != 0) {
            return 1U;
        }
        return 0U;
    }
    if (native_fn_020b3d04(arg0, arg1, arg2, 0) != 0) {
        return 1U;
    }
    return 0U;
}
