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
extern u32 native_fn_0202b524();
extern u8 native_data_020dd580[];
extern u8 native_data_020edd54[];
extern u8 native_data_020edd64[];
u32 native_main_0202a2a0(s8 arg0) {
    s32 temp_r2;
    s8 var_r0;
    u32 var_r1;

    var_r0 = arg0;
    var_r1 = 0;
    if (var_r0 != -1) {
        goto block_2;
    }
    var_r0 = (s8) *native_data_020dd580;
block_2:
    if ((u32) (u8) var_r0 >= 0x10U) {
        goto block_6;
    }
    temp_r2 = var_r0 * 0x14;
    if (*(u32 *)(native_data_020edd64 + temp_r2) == 0) {
        goto block_5;
    }
    var_r1 = native_fn_0202b524(M2C_FIELD((native_data_020edd64 + temp_r2), s32 *, 0x10));
    M2C_FIELD(native_data_020edd54, s8 *, 2) = 0;
    goto block_7;
block_5:
    M2C_FIELD(native_data_020edd54, s8 *, 2) = 1;
    goto block_7;
block_6:
    M2C_FIELD(native_data_020edd54, s8 *, 2) = 1;
block_7:
    return var_r1;
}
