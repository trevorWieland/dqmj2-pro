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
extern u32 native_fn_02040434();
extern u32 native_fn_020404f0();
extern u32 native_fn_0205bd4c();
extern u32 native_fn_ov000_021e4e9c();
extern u32 native_fn_ov000_021e52c0();
typedef struct {
    u8 unknown_0[0x1f];
    u8 field_1f;
} Record_native_data_020f6054;
extern Record_native_data_020f6054 native_data_020f6054;
u32 native_main_0203e210(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_020f6054.field_1f == 0) {
        if (!(native_fn_ov000_021e4e9c(0x8C) == 0)) {
            native_data_020f6054.field_1f = 0xAU;
        } else {
            native_data_020f6054.field_1f = 0x32U;
        }
    }
    if ((native_data_020f6054.field_1f == 0xA) && (native_fn_ov000_021e52c0() != 0)) {
        native_fn_0205bd4c();
        native_data_020f6054.field_1f = 0x32U;
    }
    if (native_data_020f6054.field_1f == 0x32) {
        native_fn_020404f0(0x12);
        native_data_020f6054.field_1f = 0U;
        var_r4 = 1;
    }
    if (native_data_020f6054.field_1f == 0x3C) {
        native_fn_020404f0(5);
        native_data_020f6054.field_1f = 0U;
        var_r4 = 1;
    }
    native_fn_02040434();
    return var_r4;
}
