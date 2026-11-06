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
extern u32 native_fn_0208522c();
void native_main_020851d4(void) {
    u8 var_r5;

    var_r5 = 0;
loop_1:
    native_fn_0208522c(1, var_r5);
    var_r5 += 1;
    if ((u32) var_r5 < 0x23U) {
        goto loop_1;
    }
    return;
}
