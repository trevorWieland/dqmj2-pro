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
extern u32 native_fn_02003b1c();
extern u8 native_data_020e3320[];
u32 native_main_02005158(void) {
    u32 temp_r0;

    temp_r0 = native_fn_02003b1c();
    M2C_FIELD(native_data_020e3320, u32 *, 0x14) = temp_r0;
    if ((s32) temp_r0 > 0x20) {
        goto block_6;
    }
    if ((s32) temp_r0 >= 0x20) {
        goto block_13;
    }
    if ((s32) temp_r0 > 0) {
        goto block_4;
    }
    return temp_r0;
block_4:
    if (temp_r0 == 0x10) {
        goto block_11;
    }
    return temp_r0;
block_6:
    if ((s32) temp_r0 > 0x40) {
        goto block_9;
    }
    if (temp_r0 == 0x40) {
        goto block_12;
    }
    return temp_r0;
block_9:
    if (temp_r0 == 0x60) {
        goto block_13;
    }
    return temp_r0;
block_11:
    M2C_FIELD(native_data_020e3320, s32 *, 0x10) = 0x06880000;
    M2C_FIELD(native_data_020e3320, s32 *, 0xC) = 0;
    return 0U;
block_12:
    M2C_FIELD(native_data_020e3320, s32 *, 0x10) = 0x06894000;
    M2C_FIELD(native_data_020e3320, s32 *, 0xC) = 0x4000;
    return 0x4000U;
block_13:
    M2C_FIELD(native_data_020e3320, s32 *, 0x10) = 0x06890000;
    M2C_FIELD(native_data_020e3320, s32 *, 0xC) = 0;
    return (u32) native_data_020e3320;
}
