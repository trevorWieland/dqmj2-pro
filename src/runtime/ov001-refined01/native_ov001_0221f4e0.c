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
extern u32 native_fn_0207b004();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_022180e0();
u32 native_ov001_0221f4e0(void *arg0) {
    s32 var_r4;
    s32 var_r5;
    s32 temp_r6;
    void *var_r7;
    s32 var_r8;
    void *temp_r9;

    temp_r6 = M2C_FIELD(arg0, s32 *, 0xC);
    var_r7 = M2C_FIELD(arg0, void **, 8);
    var_r5 = 0;
loop_1:
    if ((ov001_record_is_active_021db8d0(var_r7) != 0) && (M2C_FIELD(var_r7, s8 *, 0x23E) == 0) && ((u32) M2C_FIELD((M2C_FIELD(var_r7, s32 *, 0x1E8) + M2C_FIELD((void *) native_fn_0207afec(temp_r6), u8 *, 0x1F)), u8 *, 0x86) <= 1U)) {
        if (M2C_FIELD(var_r7, u8 *, 0x322) != 1) {
            var_r4 = 0;
            if ((s32) M2C_FIELD(var_r7, u8 *, 0x323) > 0) {
loop_7:
                temp_r9 = var_r7 + var_r4;
                if ((native_fn_0207b004(M2C_FIELD(temp_r9, u8 *, 0x35E), 8) != 0) && (M2C_FIELD((void *) native_fn_ov001_022180e0(M2C_FIELD(temp_r9, u8 *, 0x35E)), u8 *, 4) & 4)) {
                    return 1U;
                }
                var_r4 += 1;
                if (var_r4 >= (s32) M2C_FIELD(var_r7, u8 *, 0x323)) {
                    goto block_17;
                }
                goto loop_7;
            }
            goto block_17;
        }
        var_r8 = 0;
loop_13:
        if ((native_fn_0207b004(M2C_FIELD((M2C_FIELD(var_r7, s32 *, 0x1E8) + var_r8), u8 *, 8), 8) != 0) && (M2C_FIELD((void *) native_fn_ov001_022180e0(M2C_FIELD((M2C_FIELD(var_r7, s32 *, 0x1E8) + var_r8), u8 *, 8)), u8 *, 4) & 4)) {
            return 1U;
        }
        var_r8 += 1;
        if (var_r8 >= 6) {
            goto block_17;
        }
        goto loop_13;
    }
block_17:
    var_r5 += 1;
    var_r7 += 0x440;
    if (var_r5 >= 3) {
        return 0U;
    }
    goto loop_1;
}
