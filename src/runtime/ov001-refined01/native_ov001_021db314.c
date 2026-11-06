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
extern u32 native_fn_0203caa4();
extern u32 native_fn_0203cac8();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
    u8 field_3;
} Record_native_data_ov001_022355e4;
extern Record_native_data_ov001_022355e4 native_data_ov001_022355e4;
extern u8 native_data_ov001_022362ac[];
extern u8 native_data_ov001_02236f6c[];
u32 native_ov001_021db314(void) {
    s32 var_r4;
    u8 *var_r4_2;
    u32 var_r5;
    s32 var_r6_2;
    u8 *var_r6;

    var_r5 = 0;
    var_r4 = 0;
    var_r6 = native_data_ov001_02236f6c;
    if ((s32) native_data_ov001_022355e4.field_3 > 0) {
        do {
            if ((M2C_FIELD(var_r6, u8 *, 0x31C) != 0) && (M2C_FIELD(var_r6, u8 *, 0x31D) != 0)) {
                if (M2C_FIELD(var_r6, u8 *, 0x10C) != 0) {
                    native_fn_0203cac8(var_r6 + 0x100, 0x41);
                }
                native_fn_0203caa4(var_r6, 0x41);
                var_r5 += 1;
            }
            var_r4 += 1;
            var_r6 += 0x440;
        } while (var_r4 < (s32) native_data_ov001_022355e4.field_3);
    }
    var_r4_2 = native_data_ov001_022362ac;
    var_r6_2 = 0;
    if ((s32) native_data_ov001_022355e4.field_2 > 0) {
        do {
            if ((M2C_FIELD(var_r4_2, u8 *, 0x31C) != 0) && (M2C_FIELD(var_r4_2, u8 *, 0x31D) != 0)) {
                if (M2C_FIELD(var_r4_2, u8 *, 0x10C) != 0) {
                    native_fn_0203cac8(var_r4_2 + 0x100, 0x41);
                }
                native_fn_0203caa4(var_r4_2, 0x41);
                var_r5 += 1;
            }
            var_r6_2 += 1;
            var_r4_2 += 0x440;
        } while (var_r6_2 < (s32) native_data_ov001_022355e4.field_2);
    }
    return var_r5;
}
