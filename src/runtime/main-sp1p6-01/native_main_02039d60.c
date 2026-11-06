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
extern u32 native_fn_02007074();
extern u32 native_fn_0200bd04();
extern u32 native_fn_0202b9dc();
extern u32 native_fn_0202ba20();
extern u32 native_fn_02039e64();
extern u32 native_fn_0203a6ac();
extern u32 native_fn_0203b560();
extern u8 native_data_020f4c84[];
extern u8 native_data_020f4c90[];
extern u8 native_data_020f4c9c[];
extern u8 native_data_020f4cb4[];
extern u8 native_data_020f4e40[];
extern u8 native_data_020f5040[];
extern u8 native_data_020f552c[];
u32 native_main_02039d60(u32 arg0, u32 arg1) {
    s32 var_r5;
    s32 temp_r6;
    s32 var_r9;

    if (M2C_FIELD(native_data_020f4c84, s32 *, 0) == 0) {
        goto block_2;
    }
    return native_fn_02039e64(arg1);
block_2:
    M2C_FIELD(native_data_020f4c84, s32 *, 0) = 1;
    native_fn_0202b9dc(native_data_020f4c90, 0);
    var_r9 = 0;
    goto loop_4;
block_3:
    native_fn_0202ba20(native_data_020f4c90, (var_r9 * 0x30) + (s32) native_data_020f4cb4);
    var_r9 += 1;
loop_4:
    if (var_r9 < 8) {
        goto block_3;
    }
    native_fn_02007074(native_data_020f4c9c);
    var_r5 = 0;
    M2C_FIELD(native_data_020f4c84, u8 **, 8) = native_data_020f4e40;
    goto loop_7;
block_6:
    temp_r6 = (var_r5 * 0x174) + (s32) native_data_020f552c;
    M2C_FIELD(temp_r6, s32 *, 0x110) = (s32) (M2C_FIELD(temp_r6, s32 *, 0x110) & ~1);
    native_fn_0200bd04(temp_r6 + 0x5C);
    native_fn_0203b560(temp_r6);
    M2C_FIELD(temp_r6, s32 *, 0x148) = var_r5;
    M2C_FIELD(temp_r6, s8 *, 0x124) = 0;
    M2C_FIELD(temp_r6, s32 *, 0x12C) = 0;
    M2C_FIELD(temp_r6, s32 *, 0x130) = 0;
    M2C_FIELD(temp_r6, s32 *, 0x120) = 0;
    var_r5 += 1;
loop_7:
    if (var_r5 < 4) {
        goto block_6;
    }
    native_fn_02039e64(arg1);
    return native_fn_0203a6ac(native_data_020f5040, arg0);
}
