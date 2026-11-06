#define NULL ((void *)0)
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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02037b94();
extern u32 native_fn_02038fe0();
extern u32 native_fn_0203a554();
extern u32 native_fn_0203a838();
extern u8 native_data_020f552c[];
u32 native_main_02039e64(s32 arg0) {
    u32 temp_r0_2;
    u8 *temp_r0;
    s32 var_r1;
    u8 *temp_r2;
    u8 temp_r3;
    s32 var_r7;
    s32 temp_r8;
    u8 *var_r9;

    var_r7 = 0;
    var_r9 = native_data_020f552c;
loop_1:
    temp_r0 = native_fn_02038fe0(var_r7);
    if (temp_r0 != NULL) {
        var_r1 = 0;
        M2C_FIELD(var_r9, u8 *, 0x124) = (u8) *temp_r0;
        if ((s32) *temp_r0 > 0) {
            do {
                temp_r3 = M2C_FIELD(&temp_r0[var_r1], u8 *, 1);
                temp_r2 = &var_r9[var_r1];
                var_r1 += 1;
                M2C_FIELD(temp_r2, u8 *, 0x126) = temp_r3;
            } while (var_r1 < (s32) *temp_r0);
        }
        if (arg0 != 0) {
            temp_r8 = M2C_FIELD(var_r9, u8 *, 0x124) << 0xB;
            temp_r0_2 = native_fn_02037b94(arg0, temp_r8, native_fn_0203a838, var_r9, 0);
            if (temp_r0_2 == 0) {
                return 0U;
            }
            native_fn_0203a554(var_r9);
            M2C_FIELD(var_r9, u32 *, 0x12C) = temp_r0_2;
            M2C_FIELD(var_r9, s32 *, 0x130) = temp_r8;
            goto block_8;
        }
        goto block_8;
    }
block_8:
    var_r7 += 1;
    var_r9 += 0x174;
    if (var_r7 >= 4) {
        return 1U;
    }
    goto loop_1;
}
