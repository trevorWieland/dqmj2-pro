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
extern u32 native_fn_02044dc4();
extern u32 native_fn_02062a10();
extern u32 native_fn_02067748();
u32 native_main_020ced60(s32 arg0) {
    s32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u32 temp_r0_5;
    u32 temp_r0_6;
    u32 temp_r0_7;
    u8 var_r5;
    u8 var_r5_2;
    u8 var_r5_3;

    temp_r0 = M2C_FIELD((void *) native_fn_02067748(), s32 *, 4);
    if (temp_r0 == 1) {
        goto block_4;
    }
    if (temp_r0 == 2) {
        goto block_12;
    }
    if (temp_r0 == 3) {
        goto block_20;
    }
    goto block_26;
block_4:
    var_r5 = 0;
loop_5:
    temp_r0_2 = native_fn_02062a10(M2C_FIELD((arg0 + (var_r5 * 4)), s32 *, 0x18));
    if (temp_r0_2 == 0) {
        goto block_26;
    }
    temp_r0_3 = native_fn_02044dc4(M2C_FIELD(temp_r0_2, s16 *, 0x18), M2C_FIELD(temp_r0_2, u8 *, 0x1A));
    if (temp_r0_3 == 1) {
        goto block_10;
    }
    if (temp_r0_3 == 2) {
        goto block_10;
    }
    if (temp_r0_3 == 3) {
        goto block_10;
    }
    return 1U;
block_10:
    var_r5 += 1;
    if ((u32) var_r5 < 3U) {
        goto loop_5;
    }
    goto block_26;
block_12:
    var_r5_2 = 0;
loop_13:
    temp_r0_4 = native_fn_02062a10(M2C_FIELD((arg0 + (var_r5_2 * 4)), s32 *, 0x18));
    if (temp_r0_4 == 0) {
        goto block_26;
    }
    temp_r0_5 = native_fn_02044dc4(M2C_FIELD(temp_r0_4, s16 *, 0x18), M2C_FIELD(temp_r0_4, u8 *, 0x1A));
    if (temp_r0_5 == 4) {
        goto block_18;
    }
    if (temp_r0_5 == 5) {
        goto block_18;
    }
    if (temp_r0_5 == 6) {
        goto block_18;
    }
    return 1U;
block_18:
    var_r5_2 += 1;
    if ((u32) var_r5_2 < 3U) {
        goto loop_13;
    }
    goto block_26;
block_20:
    var_r5_3 = 0;
loop_21:
    temp_r0_6 = native_fn_02062a10(M2C_FIELD((arg0 + (var_r5_3 * 4)), s32 *, 0x18));
    if (temp_r0_6 == 0) {
        goto block_26;
    }
    temp_r0_7 = native_fn_02044dc4(M2C_FIELD(temp_r0_6, s16 *, 0x18), M2C_FIELD(temp_r0_6, u8 *, 0x1A));
    if (temp_r0_7 == 7) {
        goto block_25;
    }
    if (temp_r0_7 == 8) {
        goto block_25;
    }
    return 1U;
block_25:
    var_r5_3 += 1;
    if ((u32) var_r5_3 < 3U) {
        goto loop_21;
    }
block_26:
    return 0U;
}
