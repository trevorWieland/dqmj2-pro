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
extern u32 native_fn_02012290();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02083670();
extern u32 native_fn_02083718();
u32 native_main_020835d4(u16 arg0) {
    u16 var_r4;
    u32 temp_r0;

    var_r4 = arg0;
    temp_r0 = native_fn_02012290();
    if (temp_r0 != 0x8000) {
        goto block_2;
    }
    native_fn_020824c4(3);
    native_fn_020824b4(9);
    return 3U;
block_2:
    if (temp_r0 != 0) {
        goto block_4;
    }
    native_fn_020824c4(0x16);
    native_fn_020824b4(9);
    return 0x18U;
block_4:
    if (temp_r0 & (1 << (var_r4 - 1))) {
        goto block_8;
    }
loop_5:
    var_r4 += 1;
    if ((u32) var_r4 <= 0x10U) {
        goto block_7;
    }
    return 0x18U;
block_7:
    if (!(temp_r0 & (1 << (var_r4 - 1)))) {
        goto loop_5;
    }
block_8:
    return (u32) (u16) native_fn_02083718(native_fn_02083670, var_r4);
}
