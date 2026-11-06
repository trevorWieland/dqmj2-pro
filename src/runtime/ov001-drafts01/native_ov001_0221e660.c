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
extern u32 native_fn_0203d294();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dbec8();
extern u32 native_fn_ov001_02210ba8();
u32 native_ov001_0221e660(void *arg0) {
    s32 var_r5;
    u32 temp_r6;
    void *var_r7;

    var_r7 = M2C_FIELD(arg0, void **, 8);
    temp_r6 = native_fn_ov001_021dbec8(M2C_FIELD(arg0, s32 *, 0));
    var_r5 = 0;
loop_1:
    if ((native_fn_ov001_021db8d0(var_r7) != 0) && (native_fn_ov001_02210ba8(var_r7) != 0)) {
        if ((M2C_FIELD(var_r7, s8 *, 0x242) == 0) && (M2C_FIELD(var_r7, s8 *, 0x243) == 0)) {
            if ((temp_r6 != 0) || ((s32) native_fn_0203d294(0xA) < 9)) {
                return 1U;
            }
            goto block_10;
        }
        goto block_10;
    }
block_10:
    var_r5 += 1;
    var_r7 += 0x440;
    if (var_r5 >= 3) {
        return 0U;
    }
    goto loop_1;
}
