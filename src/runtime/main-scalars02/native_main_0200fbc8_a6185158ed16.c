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
extern u8 native_data_020dce4c[];
u32 native_main_0200fbc8(void *arg0) {
    s32 var_r2;
    u32 temp_r1;
    u32 temp_r2;
    u32 temp_r3;

    temp_r3 = M2C_FIELD(arg0, u32 *, 0);
    if (temp_r3 >= 0x64U) {
        goto block_8;
    }
    temp_r2 = M2C_FIELD(arg0, u32 *, 4);
    if (temp_r2 < 1U) {
        goto block_8;
    }
    if (temp_r2 > 0xCU) {
        goto block_8;
    }
    temp_r1 = M2C_FIELD(arg0, u32 *, 8);
    if (temp_r1 < 1U) {
        goto block_8;
    }
    if (temp_r1 > 0x1FU) {
        goto block_8;
    }
    if ((s32) M2C_FIELD(arg0, s32 *, 0xC) >= 7) {
        goto block_8;
    }
    if (temp_r2 < 1U) {
        goto block_8;
    }
    if (temp_r2 <= 0xCU) {
        goto block_9;
    }
block_8:
    return -1U;
block_9:
    var_r2 = (temp_r1 - 1) + *(u32 *)(native_data_020dce4c + (temp_r2 * 4));
    if (temp_r2 < 3U) {
        goto block_12;
    }
    if (temp_r3 & 3) {
        goto block_12;
    }
    var_r2 += 1;
block_12:
    return (temp_r3 * 0x16D) + var_r2 + ((u32) (temp_r3 + 3) >> 2);
}
