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
extern u32 native_fn_0203d138();
u32 native_main_02026d74(void) {
    u32 temp_r0;

    temp_r0 = *(s32 *)0x027FFC20 & 0xF0000000;
    if (temp_r0 > 0x40000000U) {
        goto block_8;
    }
    if (temp_r0 >= 0x40000000U) {
        goto block_18;
    }
    if (temp_r0 > 0x20000000U) {
        goto block_6;
    }
    if (temp_r0 >= 0x20000000U) {
        goto block_17;
    }
    if (temp_r0 == 0x10000000) {
        goto block_17;
    }
    goto block_20;
block_6:
    if (temp_r0 == 0x30000000) {
        goto block_17;
    }
    goto block_20;
block_8:
    if (temp_r0 > 0x60000000U) {
        goto block_12;
    }
    if (temp_r0 >= 0x60000000U) {
        goto block_17;
    }
    if (temp_r0 == 0x50000000) {
        goto block_17;
    }
    goto block_20;
block_12:
    if (temp_r0 > 0x70000000U) {
        goto block_15;
    }
    if (temp_r0 == 0x70000000) {
        goto block_19;
    }
    goto block_20;
block_15:
    if (temp_r0 == 0x80000000) {
        goto block_18;
    }
    goto block_20;
block_17:
    return 8U;
block_18:
    native_fn_0203d138(7);
    return 0xBU;
block_19:
    return 7U;
block_20:
    native_fn_0203d138(7);
    return 0xBU;
}
