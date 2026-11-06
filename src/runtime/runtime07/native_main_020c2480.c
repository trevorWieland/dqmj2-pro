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
extern u32 native_fn_02006b7c();
extern u32 native_fn_0205fd34();
extern u32 native_fn_0205fd60();
extern u32 native_fn_0205fd70();
u32 native_main_020c2480(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    temp_r0_3 = native_fn_0205fd60();
    if (temp_r0_3 == 0) {
        return temp_r0_3;
    }
loop_3:
    temp_r0_2 = native_fn_0205fd70();
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    native_fn_0205fd34(temp_r0_2, 0x10);
    native_fn_02006b7c(0xA);
    temp_r0 = native_fn_0205fd60();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    goto loop_3;
}
