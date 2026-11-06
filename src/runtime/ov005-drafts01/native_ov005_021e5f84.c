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
extern u32 native_fn_0201b248();
typedef struct {
    u8 unknown_0[0x40];
    s32 field_40;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e5f84(u32 arg0) {
    u32 var_r5;
    s32 var_r6;
    s32 var_r7;

    var_r5 = 0;
    var_r6 = 0;
    var_r7 = native_data_ov005_021ed438.field_40 + 0xF8;
loop_1:
    if (native_fn_0201b248(var_r7, arg0, 6) == 0) {
        var_r5 = 1;
    } else {
        var_r6 += 1;
        var_r7 += 0x268;
        if (var_r6 < 0xA) {
            goto loop_1;
        }
    }
    return var_r5;
}
