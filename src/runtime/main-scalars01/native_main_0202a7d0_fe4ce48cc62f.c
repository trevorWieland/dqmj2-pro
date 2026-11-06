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
extern u32 native_fn_02008c58();
extern u32 native_fn_0200bcdc();
extern u8 native_data_020edec8[];
extern u8 native_data_020edecc[];
u32 native_main_0202a7d0(s32 arg0) {
    s32 var_r0;

    var_r0 = arg0;
    if (var_r0 != 5) {
        goto block_2;
    }
    var_r0 = -1;
    goto block_4;
block_2:
    if (var_r0 != 4) {
        goto block_4;
    }
    var_r0 = 3;
block_4:
    native_fn_0200bcdc(var_r0);
    native_fn_02008c58(0, native_data_020edecc, 0x54);
    *(u32 *)native_data_020edec8 = 0;
    return 1U;
}
