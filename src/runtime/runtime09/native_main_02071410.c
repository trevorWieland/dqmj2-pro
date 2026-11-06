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
extern u32 native_fn_0206dca4();
extern u8 native_data_021c4f60[];
u32 native_main_02071410(void) {
    s32 temp_r4;
    s32 var_r5;

    var_r5 = 0;
    temp_r4 = M2C_FIELD(native_data_021c4f60, s32 *, 0x20);
    if (M2C_FIELD(native_data_021c4f60, s8 *, 0x2F) == 0) {
        goto block_2;
    }
    return 1U;
block_2:
    if (native_fn_0206dca4() == 0) {
        goto block_7;
    }
    goto loop_5;
block_4:
    var_r5 = (s32) (s8) (var_r5 + 1);
loop_5:
    if (var_r5 >= 5) {
        goto block_7;
    }
    if (M2C_FIELD((temp_r4 + (var_r5 * 2)), u8 *, 0x7A) != 0) {
        goto block_4;
    }
block_7:
    if (var_r5 > 1) {
        goto block_9;
    }
    var_r5 = 1;
block_9:
    return (u32) (s8) var_r5;
}
