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
extern u32 native_fn_02080a10();
extern u32 native_fn_02081548();
extern u8 native_data_021c6dfc[];
u32 native_main_020814dc(u32 arg0) {
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_021c6dfc, s16 *, 6) != 0) {
        goto block_3;
    }
    if (native_fn_02081548() == 0) {
        goto block_3;
    }
    var_r4 = native_fn_02080a10(arg0);
    M2C_FIELD(native_data_021c6dfc, s16 *, 6) = 8;
block_3:
    M2C_FIELD(native_data_021c6dfc, s16 *, 6) = (s16) (M2C_FIELD(native_data_021c6dfc, s16 *, 6) - 1);
    if ((s32) M2C_FIELD(native_data_021c6dfc, s16 *, 6) >= 0) {
        goto block_5;
    }
    M2C_FIELD(native_data_021c6dfc, s16 *, 6) = 0;
block_5:
    return var_r4;
}
