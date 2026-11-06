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
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021db8d0();
u32 native_ov001_0221a03c(void *arg0) {
    s32 temp_r1;
    void *temp_r4;
    s32 temp_r5;
    s32 var_r5;
    void *var_r6;
    u8 temp_r7;
    u8 temp_r8;

    temp_r5 = M2C_FIELD(arg0, s32 *, 0xC);
    temp_r4 = M2C_FIELD(arg0, void **, 0);
    var_r6 = M2C_FIELD(arg0, void **, 8);
    temp_r7 = M2C_FIELD((void *) native_fn_0207afec(temp_r5), u8 *, 0x1F);
    temp_r8 = M2C_FIELD((void *) native_fn_0207afec(temp_r5), u8 *, 0x20);
    var_r5 = 0;
loop_1:
    if ((native_fn_ov001_021db8d0(var_r6) != 0) && (M2C_FIELD(var_r6, s8 *, 0x24D) != 0)) {
        temp_r1 = M2C_FIELD(temp_r4, s32 *, 0x1E8);
        if (((u32) M2C_FIELD((temp_r7 + temp_r1), u8 *, 0x86) <= 2U) || ((temp_r8 != 0) && ((u32) M2C_FIELD((temp_r8 + temp_r1), u8 *, 0x86) <= 2U))) {
            return 1U;
        }
        goto block_9;
    }
block_9:
    var_r5 += 1;
    var_r6 += 0x440;
    if (var_r5 >= 3) {
        return 0U;
    }
    goto loop_1;
}
