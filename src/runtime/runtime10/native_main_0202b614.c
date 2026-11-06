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
extern u32 native_fn_02008c14();
extern u32 native_fn_0202b9cc();
u32 native_main_0202b614(void *arg0, s32 arg1, s32 arg2) {
    s32 temp_r0;
    u32 temp_r3;
    u32 temp_r5;
    s32 temp_r6;

    temp_r3 = M2C_FIELD(arg0, u32 *, 4);
    temp_r5 = ~(arg2 - 1) & (temp_r3 - arg1);
    if (temp_r5 < (u32) M2C_FIELD(arg0, u32 *, 0)) {
        return 0U;
    }
    temp_r0 = M2C_FIELD(arg0, s32 *, -4);
    temp_r6 = temp_r3 - temp_r5;
    if ((u8) temp_r0 & 1) {
        native_fn_02008c14(0U, temp_r5, temp_r6);
    } else if ((u8) temp_r0 & 2) {
        native_fn_02008c14(native_fn_0202b9cc(1), temp_r5, temp_r6);
    }
    M2C_FIELD(arg0, u32 *, 4) = temp_r5;
    return temp_r5;
}
