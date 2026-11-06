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
extern u32 native_fn_0206d250();
u32 native_main_0206bbb0(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u8 *, 9) == 0) {
        goto block_3;
    }
    if (M2C_FIELD(arg1, u8 *, 9) == 0) {
        goto block_3;
    }
    goto block_4;
block_3:
    goto block_11;
block_4:
    if (M2C_FIELD(arg0, u8 *, 8) != M2C_FIELD(arg1, u8 *, 8)) {
        goto block_7;
    }
    if (M2C_FIELD(arg0, u8 *, 6) != M2C_FIELD(arg1, u8 *, 6)) {
        goto block_7;
    }
    goto block_8;
block_7:
    goto block_11;
block_8:
    if ((s32) (M2C_FIELD(arg0, u8 *, 7) - native_fn_0206d250(M2C_FIELD(arg1, s8 *, 0xC))) > (s32) M2C_FIELD(arg1, u8 *, 7)) {
        goto block_11;
    }
    if ((s32) (M2C_FIELD(arg0, u8 *, 7) + native_fn_0206d250(M2C_FIELD(arg0, s8 *, 0xC))) < (s32) M2C_FIELD(arg1, u8 *, 7)) {
        goto block_11;
    }
    return 1U;
block_11:
    return 0U;
}
