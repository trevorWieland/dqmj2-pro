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
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021dbec8();
extern u32 native_fn_ov001_021e2b88();
extern u32 native_fn_ov001_021f07dc();
u32 native_ov001_021e68bc(void *arg0, void *arg1) {
    s32 var_r4_2;
    u32 temp_r4;
    void *var_r4;
    s32 var_r5;
    s32 var_r5_2;
    s32 var_r6;
    void *var_r7;
    u32 temp_r8;
    u32 var_r8;
    void *var_r9;

    var_r9 = arg1;
    var_r8 = -1U;
    var_r6 = 0;
    if ((s32) native_fn_ov001_021e2b88() > 1) {
        return 0U;
    }
    if ((M2C_FIELD(arg0, u8 *, 0x1FE) != 4) || ((s32) native_fn_ov001_021dbec8(arg0) > 0)) {
        var_r5 = 0;
        var_r7 = var_r9;
        do {
            if (ov001_record_is_active_021db8d0(var_r7) != 0) {
                temp_r4 = native_fn_ov001_021dbd24(var_r7);
                if ((s32) temp_r4 <= (s32) native_fn_ov001_021f07dc(arg0, var_r7, 0, 0, 0, 1, 0)) {
                    var_r6 += 1;
                    if (var_r6 >= 2) {
                        var_r8 = 0;
                    }
                }
            }
            var_r5 += 1;
            var_r7 += 0x440;
        } while (var_r5 < 3);
        if (var_r8 == -1U) {
            var_r5_2 = 0;
            var_r4 = var_r9;
loop_12:
            if (ov001_record_is_active_021db8d0(var_r4) != 0) {
                temp_r8 = native_fn_ov001_021dbd24(arg0);
                if ((s32) temp_r8 <= (s32) (M2C_FIELD(var_r4, u8 *, 0x356) * native_fn_ov001_021f07dc(var_r4, arg0, 0, 0, 0, 1, 0))) {
                    if (native_fn_0203d294(4) == 0) {
                        var_r8 = 1;
                    } else {
                        var_r8 = 0;
                    }
                    goto block_19;
                }
                var_r8 = -1U;
            } else {
block_19:
                var_r5_2 += 1;
                var_r4 += 0x440;
                if (var_r5_2 < 3) {
                    goto loop_12;
                }
            }
        }
        if (var_r8 == -1U) {
            var_r8 = 0;
        }
    } else {
        var_r8 = 0;
    }
    var_r4_2 = 0;
loop_25:
    if ((ov001_record_is_active_021db8d0(var_r9) != 0) && (M2C_FIELD(var_r9, s8 *, 0x24D) == 0) && (M2C_FIELD(var_r9, s8 *, 0x24C) == 0)) {
        return var_r8;
    }
    var_r4_2 += 1;
    var_r9 += 0x440;
    if (var_r4_2 >= 3) {
        return 1U;
    }
    goto loop_25;
}
