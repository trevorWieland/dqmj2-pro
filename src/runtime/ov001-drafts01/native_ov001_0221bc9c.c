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
extern u32 native_fn_ov001_021dbd24();
extern u32 ov001_record_field_1f2_021dbd30();
u32 native_ov001_0221bc9c(void *arg0) {
    s32 temp_r9;
    s32 var_r10;
    s32 var_r1;
    s32 var_r5;
    u32 temp_r0;
    u32 temp_r5;
    u8 temp_r2;
    void *var_r4;

    var_r10 = 0;
    temp_r9 = M2C_FIELD(arg0, s32 *, 0);
    var_r4 = M2C_FIELD(arg0, void **, 8);
loop_1:
    var_r5 = 0;
    if (ov001_record_is_active_021db8d0(var_r4) != 0) {
        temp_r2 = M2C_FIELD(var_r4, u8 *, 0x323);
        var_r1 = 0;
        if ((s32) temp_r2 > 0) {
loop_3:
            if (M2C_FIELD((var_r4 + var_r1), u8 *, 0x35E) == 0x5F) {
                var_r5 = 1;
            } else {
                var_r1 += 1;
                if (var_r1 < (s32) temp_r2) {
                    goto loop_3;
                }
            }
        }
        if (var_r5 != 0) {
            temp_r5 = native_fn_ov001_021dbd24(temp_r9);
            temp_r0 = ov001_record_field_1f2_021dbd30(var_r4) * 3;
            if ((s32) temp_r5 <= (s32) ((s32) (temp_r0 + (temp_r0 >> 0x1F)) >> 1)) {
                return 1U;
            }
        }
        goto block_9;
    }
block_9:
    var_r10 += 1;
    var_r4 += 0x440;
    if (var_r10 >= 3) {
        return 0U;
    }
    goto loop_1;
}
