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
extern u32 native_fn_ov001_021d8dec();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_0222096c();
extern u32 native_fn_ov001_022209ac();
extern u32 native_fn_ov001_022209ec();
u32 native_ov001_0221c674(void *arg0) {
    s32 temp_r7;
    s32 var_r8;
    s32 var_r9;
    void *var_r10;

    var_r8 = 0;
    temp_r7 = M2C_FIELD(arg0, s32 *, 8);
loop_1:
    var_r10 = temp_r7 + (var_r8 * 0x440);
    if (ov001_record_is_active_021db8d0(var_r10) != 0) {
        var_r9 = 0;
loop_3:
        if ((M2C_FIELD((void *) native_fn_ov001_021d8dec(var_r9), u8 *, 3) & 4) && (M2C_FIELD(var_r10, s8 *, 0x22C) != 0) && (M2C_FIELD(var_r10, s8 *, 0x268) != -2)) {
            if ((M2C_FIELD((void *) native_fn_ov001_021d8dec(var_r9), s8 *, 8) == 0) || ((M2C_FIELD((void *) native_fn_ov001_021d8dec(var_r9), s8 *, 8) == 2) && ((s32) M2C_FIELD(var_r10, s8 *, 0x22C) > 0))) {
                var_r8 = 3;
            } else {
                goto block_12;
            }
        } else {
block_12:
            var_r9 += 1;
            var_r10 += 1;
            if (var_r9 < 0x3C) {
                goto loop_3;
            }
        }
    }
    if (var_r8 == 2) {
        if ((native_fn_ov001_0222096c(arg0) == 0) && (native_fn_ov001_022209ac(arg0) == 0) && (native_fn_ov001_022209ec(arg0) == 0)) {
            return 1U;
        }
        return 0U;
    }
    var_r8 += 1;
    if (var_r8 >= 3) {
        return 0U;
    }
    goto loop_1;
}
