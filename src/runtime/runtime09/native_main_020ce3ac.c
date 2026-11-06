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
extern u32 native_fn_02062850();
extern u32 native_fn_020628b0();
extern u32 native_fn_02062904();
extern u32 native_fn_02062980();
extern u32 native_fn_02062a68();
extern u32 native_fn_02062a78();
extern u32 native_fn_02063fa0();
extern u32 native_fn_02063fac();
extern u32 native_fn_020cc740();
extern u32 native_fn_020ced10();
extern u32 native_fn_020cf27c();
extern u8 native_data_021d69a0[];
u32 native_main_020ce3ac(void) {
    u32 temp_r0;
    u32 temp_r5;
    u8 temp_r4;
    u8 var_r4;
    u8 var_r4_2;
    u8 var_r6;
    u8 var_r6_2;
    u8 var_r6_3;
    u8 var_r6_4;
    u8 var_r9;
    u8 var_r9_2;

    temp_r4 = (u8) *(s32 *) native_fn_020cc740();
    temp_r0 = native_fn_020cf27c();
    temp_r5 = temp_r0;
    if (temp_r4 == 0) {
        goto block_3;
    }
    if (temp_r4 == 1) {
        goto block_15;
    }
    return temp_r0;
block_3:
    var_r6 = 0;
loop_4:
    native_fn_020628b0(0U);
    var_r6 += 1;
    if ((u32) var_r6 < 3U) {
        goto loop_4;
    }
    var_r6_2 = 0;
loop_6:
    if (native_fn_02063fac(M2C_FIELD((temp_r5 + (var_r6_2 * 4)), s32 *, 0x18)) == 0) {
        goto block_11;
    }
    var_r9 = 0;
loop_8:
    if (M2C_FIELD((temp_r5 + (var_r6_2 * 4)), s32 *, 0x18) != native_fn_02062a78(var_r9)) {
        goto block_10;
    }
    native_fn_02062980(var_r9);
    var_r9 = 0;
block_10:
    var_r9 += 1;
    if ((u32) var_r9 < 3U) {
        goto loop_8;
    }
block_11:
    var_r6_2 += 1;
    if ((u32) var_r6_2 < 3U) {
        goto loop_6;
    }
    var_r4 = 0;
loop_13:
    native_fn_02062850(M2C_FIELD((temp_r5 + (var_r4 * 4)), s32 *, 0x18));
    var_r4 += 1;
    if ((u32) var_r4 < 3U) {
        goto loop_13;
    }
    native_fn_020ced10(temp_r5, 0, 9);
    M2C_FIELD(native_data_021d69a0, s32 *, 4) = 1;
    return (u32) native_data_021d69a0;
block_15:
    var_r6_3 = 0;
loop_16:
    native_fn_02062980(0U);
    var_r6_3 += 1;
    if ((u32) var_r6_3 < 3U) {
        goto loop_16;
    }
    var_r6_4 = 0;
loop_18:
    if (native_fn_02063fa0(M2C_FIELD((temp_r5 + (var_r6_4 * 4)), s32 *, 0x18)) == 0) {
        goto block_23;
    }
    var_r9_2 = 0;
loop_20:
    if (M2C_FIELD((temp_r5 + (var_r6_4 * 4)), s32 *, 0x18) != native_fn_02062a68(var_r9_2)) {
        goto block_22;
    }
    native_fn_020628b0(var_r9_2);
    var_r9_2 = 0;
block_22:
    var_r9_2 += 1;
    if ((u32) var_r9_2 < 3U) {
        goto loop_20;
    }
block_23:
    var_r6_4 += 1;
    if ((u32) var_r6_4 < 3U) {
        goto loop_18;
    }
    var_r4_2 = 0;
loop_25:
    native_fn_02062904(M2C_FIELD((temp_r5 + (var_r4_2 * 4)), s32 *, 0x18));
    var_r4_2 += 1;
    if ((u32) var_r4_2 < 3U) {
        goto loop_25;
    }
    native_fn_020ced10(temp_r5, 0, 0xA);
    M2C_FIELD(native_data_021d69a0, s32 *, 4) = 1;
    return (u32) native_data_021d69a0;
}
