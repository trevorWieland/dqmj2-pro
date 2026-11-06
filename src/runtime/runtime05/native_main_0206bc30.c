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
extern u32 native_fn_0206bbb0();
extern u8 native_data_021c4a04[];
u32 native_main_0206bc30(s32 arg0) {
    s32 var_r4;
    u8 *var_r5;

    var_r5 = native_data_021c4a04;
    var_r4 = 0;
loop_1:
    if ((arg0 != var_r4) && (native_fn_0206bbb0(var_r5, native_data_021c4a04 + (arg0 * 0x10)) != 0)) {
        return (u32) var_r4;
    }
    var_r4 += 1;
    var_r5 += 0x10;
    if (var_r4 >= 0xF) {
        return -1U;
    }
    goto loop_1;
}
