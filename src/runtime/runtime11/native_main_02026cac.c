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
extern u32 native_fn_02002c50();
extern u32 native_fn_0203d234();
extern u32 native_fn_020642cc();
void native_main_02026cac(void) {
    u32 temp_r0;

    native_fn_020642cc(0);
    native_fn_0203d234(1);
    temp_r0 = *(s32 *)0x027FFC20 & 0xF0000000;
    if (temp_r0 > 0x30000000U) {
        goto block_7;
    }
    if (temp_r0 >= 0x30000000U) {
        goto block_13;
    }
    if (temp_r0 > 0x10000000U) {
        goto block_5;
    }
    if (temp_r0 == 0x10000000) {
        goto block_13;
    }
    return;
block_5:
    if (temp_r0 == 0x20000000) {
        goto block_13;
    }
    return;
block_7:
    if (temp_r0 > 0x50000000U) {
        goto block_11;
    }
    if (temp_r0 >= 0x50000000U) {
        goto block_13;
    }
    if (temp_r0 == 0x40000000) {
        goto block_14;
    }
    return;
block_11:
    if (temp_r0 == 0x60000000) {
        goto block_13;
    }
    return;
block_13:
    native_fn_020642cc(0x2F);
    *(u16 *)0x04000304 = (*(u16 *)0x04000304 & 0xFFFFFDF1) | 0x20E;
    native_fn_02002c50();
    *(s32 *)0x04001000 |= 0x10000;
    native_fn_0203d234(0);
    return;
block_14:
    native_fn_0203d234(0);
    return;
}
