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
extern u8 native_data_020d8ce0[];
u32 native_main_0201626c(s32 arg0, u32 arg1, s32 arg2) {
    s32 temp_r0;

    temp_r0 = *(u32 *)(native_data_020d8ce0 + (arg0 * 4));
    if (temp_r0 == 0) {
        goto block_6;
    }
    if (temp_r0 == 1) {
        goto block_9;
    }
    if (temp_r0 != 2) {
        goto block_15;
    }
    if (arg1 < 0x027FFE00U) {
        goto block_16;
    }
    if ((u32) (arg1 + arg2) > 0x027FFF60U) {
        goto block_16;
    }
    return 1U;
block_6:
    if (arg1 < 0x02000000U) {
        goto block_16;
    }
    if ((u32) (arg1 + arg2) > 0x022C0000U) {
        goto block_16;
    }
    return 1U;
block_9:
    if (arg1 < 0x022C0000U) {
        goto block_12;
    }
    if ((u32) (arg1 + arg2) > 0x02300000U) {
        goto block_12;
    }
    return 1U;
block_12:
    if (arg1 < 0x02000000U) {
        goto block_16;
    }
    if ((u32) (arg1 + arg2) > 0x02300000U) {
        goto block_16;
    }
    return 1U;
block_15:
    return 0U;
block_16:
    return 0U;
}
