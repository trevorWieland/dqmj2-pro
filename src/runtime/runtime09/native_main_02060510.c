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
extern u32 native_fn_0203d4d0();
extern u32 native_fn_0207afec();
u32 native_main_02060510(u32 arg0) {
    u16 temp_r1;
    u16 temp_r1_2;
    u32 temp_r0;
    u32 var_r0;
    u32 var_r2;
    u32 var_r3;
    u8 var_r0_2;
    void *temp_r0_2;
    void *temp_r0_3;

    temp_r0 = native_fn_0203d4d0();
    if (temp_r0 == 0) {
        goto block_2;
    }
    if (temp_r0 == 1) {
        goto block_3;
    }
block_2:
    temp_r0_2 = (void *) native_fn_0207afec(arg0);
    temp_r1 = M2C_FIELD(temp_r0_2, u16 *, 8);
    var_r0_2 = M2C_FIELD(temp_r0_2, u8 *, 0x1E);
    var_r2 = (u32) (temp_r1 << 0x1C) >> 0x1C;
    var_r3 = (u32) (temp_r1 << 0x18) >> 0x1C;
    goto block_4;
block_3:
    temp_r0_3 = (void *) native_fn_0207afec(arg0);
    temp_r1_2 = M2C_FIELD(temp_r0_3, u16 *, 8);
    var_r0_2 = M2C_FIELD(temp_r0_3, u8 *, 0x1E);
    var_r2 = (u32) (temp_r1_2 << 0x1C) >> 0x1C;
    var_r3 = (u32) (temp_r1_2 << 0x18) >> 0x1C;
block_4:
    if (var_r2 != 6) {
        goto block_9;
    }
    if (var_r0_2 != 1) {
        goto block_13;
    }
    if (var_r3 == 1) {
        goto block_8;
    }
    if ((u32) (u16) (var_r3 + 0xFFFD) > 1U) {
        goto block_13;
    }
block_8:
    return 0x17U;
block_9:
    if (var_r0_2 != 1) {
        goto block_13;
    }
    if (var_r3 == 1) {
        goto block_12;
    }
    if ((u32) (u16) (var_r3 + 0xFFFD) > 1U) {
        goto block_13;
    }
block_12:
    return 0x16U;
block_13:
    if (var_r0_2 != 1) {
        goto block_20;
    }
    if (var_r3 == 1) {
        goto block_18;
    }
    if (var_r3 == 3) {
        goto block_18;
    }
    if (var_r3 == 4) {
        goto block_18;
    }
    var_r0 = 0x18;
    goto block_19;
block_18:
    var_r0 = 0;
block_19:
    return var_r0;
block_20:
    return 0x19U;
}
