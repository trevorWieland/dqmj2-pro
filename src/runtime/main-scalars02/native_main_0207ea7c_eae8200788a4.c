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
extern u32 native_fn_0207eaac();
extern u32 native_fn_0207ec6c();
extern u8 native_data_021c6c48[];
u32 native_main_0207ea7c(void) {
    s32 var_r2;

    var_r2 = 0;
loop_1:
    *(u32 *)(native_data_021c6c48 + (var_r2 * 4)) = 0x20;
    var_r2 += 1;
    if (var_r2 < 4) {
        goto loop_1;
    }
    native_fn_0207eaac();
    return native_fn_0207ec6c();
}
