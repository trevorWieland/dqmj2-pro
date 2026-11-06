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
extern u32 native_fn_02008e0c();
extern u32 native_fn_02049f14();
extern u32 native_fn_02049f24();
extern u32 native_fn_02049f30();
extern u8 native_data_021d5398[];
u32 native_main_020c4870(u32 arg0, s32 arg1) {
    s32 var_r5;
    u32 temp_r4;

    var_r5 = arg1;
    temp_r4 = native_fn_02049f24();
    native_fn_02049f30();
    if (var_r5 < 0x20) {
        goto block_2;
    }
    var_r5 = 0x20;
block_2:
    native_fn_02008e0c(arg0, temp_r4, var_r5 * 2);
    native_fn_02049f14(temp_r4);
    *native_data_021d5398 = 0xFE;
    return (u32) native_data_021d5398;
}
