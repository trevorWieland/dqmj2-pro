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
extern u32 native_fn_0204aeb4();
extern u32 native_fn_ov001_02202384();
extern u32 native_fn_ov001_0220269c();
typedef struct {
    u8 unknown_0[0x6];
    s8 field_6;
    u8 unknown_7[0x29];
    s32 field_30;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_021fedd0(s32 arg0) {
    s32 var_r4;
    s8 temp_r5;

    if (arg0 == 0) {
        var_r4 = 0;
    } else {
        var_r4 = 7;
    }
    native_fn_ov001_0220269c(arg0);
    temp_r5 = native_data_ov001_02239c10.field_6;
    return native_fn_0204aeb4(native_data_ov001_02239c10.field_30, 1, 3, var_r4 + temp_r5, 0, (s32) ((native_fn_ov001_02202384(arg0) - 8) << 0x15) >> 0x18, 1, 0);
}
