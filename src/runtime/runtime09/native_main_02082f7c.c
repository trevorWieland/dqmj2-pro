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
extern u32 native_fn_02012cb8();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02083000();
extern u8 native_data_021c72a0[];
extern u8 native_data_021c7334[];
extern u8 native_data_021c7400[];
u32 native_main_02082f7c(void) {
    u16 var_r0;

    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x34) == 4) {
        goto block_4;
    }
    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x34) == 6) {
        goto block_4;
    }
    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x34) == 5) {
        goto block_4;
    }
    goto block_5;
block_4:
    return 1U;
block_5:
    native_fn_020824b4(3);
    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x40) == 0) {
        goto block_7;
    }
    var_r0 = 1;
    goto block_8;
block_7:
    var_r0 = 0;
block_8:
    if (native_fn_02012cb8(native_fn_02083000, native_data_021c7400, native_data_021c7334, 1, (s32) var_r0) != 2) {
        goto block_10;
    }
    return 1U;
block_10:
    native_fn_020824c4();
    return 0U;
}
