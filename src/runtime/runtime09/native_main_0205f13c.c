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
extern u32 native_fn_02039ab0();
extern u32 native_fn_0205f0f8();
extern u32 native_fn_0205f210();
extern u8 native_data_021b8ae0[];
extern u8 native_data_021b8b10[];
u32 native_main_0205f13c(s32 arg0, s32 arg1, u32 arg2, u32 arg3) {
    s32 var_r8;
    void *temp_r4;

    var_r8 = arg0;
    M2C_FIELD(native_data_021b8ae0, u8 *, 1) = 0U;
    if (var_r8 >= 0) {
        goto block_2;
    }
    var_r8 = (s32) native_fn_0205f0f8();
block_2:
    if (var_r8 < 0) {
        goto block_6;
    }
    temp_r4 = native_data_021b8b10 + (var_r8 * 8);
    native_fn_0205f210(var_r8, 0);
    if (native_fn_02039ab0(temp_r4, arg2, -1, arg3, arg1) == 0) {
        goto block_5;
    }
    M2C_FIELD(temp_r4, s16 *, 4) = (s16) arg1;
    M2C_FIELD(temp_r4, u8 *, 7) = (u8) (M2C_FIELD(temp_r4, u8 *, 7) & ~2);
    M2C_FIELD(temp_r4, s8 *, 6) = 0x7F;
    M2C_FIELD(native_data_021b8ae0, u8 *, 1) = 0U;
    goto block_7;
block_5:
    M2C_FIELD(native_data_021b8ae0, u8 *, 1) = 6U;
    goto block_7;
block_6:
    M2C_FIELD(native_data_021b8ae0, u8 *, 1) = 7U;
block_7:
    if (M2C_FIELD(native_data_021b8ae0, u8 *, 1) == 0) {
        goto block_9;
    }
    var_r8 = -1;
block_9:
    return (u32) var_r8;
}
