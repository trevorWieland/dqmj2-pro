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
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_022189cc();
u32 native_ov001_02222da0(void *arg0) {
    s32 temp_r5;
    s32 temp_r6;
    s32 var_r7;
    void *var_r8;

    temp_r5 = M2C_FIELD(arg0, s32 *, 0);
    temp_r6 = M2C_FIELD(arg0, s32 *, 0xC);
    var_r8 = M2C_FIELD(arg0, void **, 8);
    var_r7 = 0;
loop_1:
    if ((ov001_record_is_active_021db8d0(var_r8) != 0) && (M2C_FIELD(var_r8, s8 *, 0x257) != 0)) {
        if ((s32) native_fn_ov001_022189cc(temp_r5, var_r8, temp_r6, 1) >= 5) {
            return 1U;
        }
        goto block_7;
    }
block_7:
    var_r7 += 1;
    var_r8 += 0x440;
    if (var_r7 >= 3) {
        return 0U;
    }
    goto loop_1;
}
