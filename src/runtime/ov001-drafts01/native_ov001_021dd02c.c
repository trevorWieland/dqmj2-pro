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
extern u32 native_fn_02044cdc();
extern u32 native_fn_0207b244();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_field_1f2_021dbd30();
extern u32 native_fn_ov001_021dc108();
u32 native_ov001_021dd02c(void *arg0, u32 arg1, s32 arg2) {
    s32 var_r5;
    s32 var_r6;
    u32 temp_r10;
    u32 temp_r4;
    u32 var_r7;
    u32 var_r8;

    var_r5 = 0;
    if (arg2 == 0) {
        temp_r4 = native_fn_0207b244(arg1, ov001_record_field_1f2_021dbd30(), M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46);
        if ((s32) ov001_record_field_1f2_021dbd30(arg0) >= (s32) temp_r4) {
            var_r8 = 1;
        } else {
            var_r8 = 0;
        }
    } else {
        var_r7 = ov001_side_slot_record_021db438(M2C_FIELD(arg0, u8 *, 0x31E), 0);
        var_r8 = 1;
        var_r6 = 0;
        do {
            if (native_fn_ov001_021dc108((void *) var_r7) != 0) {
                temp_r10 = native_fn_0207b244(arg1, ov001_record_field_1f2_021dbd30((void *) var_r7), M2C_FIELD(var_r7, void **, 0x1E8) + 0x46);
                if ((s32) ov001_record_field_1f2_021dbd30((void *) var_r7) < (s32) temp_r10) {
                    var_r8 = 0;
                }
                var_r5 += native_fn_02044cdc(M2C_FIELD(M2C_FIELD(var_r7, void **, 0x1E8), s16 *, 0x2A)) + 1;
            }
            var_r6 += 1;
            var_r7 += 0x440;
        } while (var_r6 < 3);
        if (var_r5 < 3) {
            var_r8 = 0;
        }
    }
    return var_r8;
}
