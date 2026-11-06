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
extern u32 native_fn_01ffa6c0();
extern u32 native_fn_01ffb4ec();
extern u32 native_fn_02008e0c();
void native_main_020889cc(u32 arg0) {
    u8 var_r6;
    u32 temp_r0;

    var_r6 = 0;
loop_1:
    temp_r0 = native_fn_01ffa6c0(var_r6, arg0);
    if (temp_r0 == 0) {
        goto block_3;
    }
    native_fn_02008e0c(temp_r0, native_fn_01ffb4ec(var_r6), 0x14);
block_3:
    var_r6 += 1;
    if ((u32) var_r6 < 8U) {
        goto loop_1;
    }
    return;
}
