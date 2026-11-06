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
extern u32 native_fn_0203d294();
extern u32 native_fn_0207d2c8();
u32 native_main_0207d650(s32 arg0, s32 arg1) {
    u32 temp_r0;
    u8 temp_r0_2;

    temp_r0 = native_fn_0207d2c8();
    if (arg0 != 0) {
        goto block_2;
    }
    return 0U;
block_2:
    if (M2C_FIELD(temp_r0, u8 *, 3) != 2) {
        goto block_10;
    }
    temp_r0_2 = M2C_FIELD(temp_r0, u8 *, 4);
    if (temp_r0_2 == 2) {
        goto block_6;
    }
    if (temp_r0_2 == 3) {
        goto block_8;
    }
    goto block_10;
block_6:
    if ((s32) native_fn_0203d294(0xC80) >= arg1) {
        goto block_10;
    }
    return 1U;
block_8:
    if ((s32) native_fn_0203d294(0x640) >= arg1) {
        goto block_10;
    }
    return 1U;
block_10:
    return 0U;
}
