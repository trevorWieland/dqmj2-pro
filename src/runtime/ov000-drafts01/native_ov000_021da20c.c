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
extern u32 native_fn_0203ca88();
extern u32 native_fn_0203caa4();
extern u8 native_data_ov000_0223042c[];
extern u8 native_data_ov000_022304ec[];
extern u8 native_data_ov000_022305ec[];
u32 native_ov000_021da20c(s32 arg0) {
    s32 var_r5;
    u32 var_r6;
    u8 *var_r7;
    u8 *var_r8;
    u8 *var_r9;

    var_r7 = native_data_ov000_0223042c;
    var_r6 = 0;
    var_r5 = 0;
    if ((s32) M2C_FIELD(native_data_ov000_0223042c, s32 *, 0x58) > 0) {
        var_r8 = native_data_ov000_022305ec;
        var_r9 = native_data_ov000_022304ec;
        do {
            if ((arg0 == M2C_FIELD(var_r7, u8 *, 0x1CC)) && (M2C_FIELD(var_r7, u8 *, 0x1CE) != 0)) {
                native_fn_0203ca88(var_r8, 0);
                native_fn_0203caa4(var_r9, 0);
                var_r6 += 1;
            }
            var_r5 += 1;
            var_r7 += 0x174;
            var_r8 += 0x174;
            var_r9 += 0x174;
        } while (var_r5 < (s32) M2C_FIELD(native_data_ov000_0223042c, s32 *, 0x58));
    }
    return var_r6;
}
