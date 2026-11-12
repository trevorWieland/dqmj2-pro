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
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021dc230();
u32 native_ov001_021dbb14(u32 arg0, u32 arg1) {
    s32 var_r6;
    s32 var_r7;
    u32 var_r8;
    u32 var_r9;

    var_r9 = arg0;
    var_r8 = 0;
    if (var_r9 != 0) {
        var_r7 = 1;
    } else {
        var_r9 = ov001_side_slot_record_021db438(arg1, 0);
        var_r7 = 3;
    }
    var_r6 = 0;
    if ((var_r7 > 0) && (var_r7 > 0)) {
        do {
            if ((ov001_record_is_active_021db8d0(var_r9) != 0) && ((s32) native_fn_ov001_021dbd24(var_r9) <= 0)) {
                native_fn_ov001_021dc230(var_r9, 1);
                var_r8 = 1;
            }
            var_r6 += 1;
            var_r9 += 0x440;
        } while (var_r6 < var_r7);
    }
    return var_r8;
}
