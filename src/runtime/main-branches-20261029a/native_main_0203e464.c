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
extern u32 native_fn_02041800();
extern u32 native_fn_0205bd4c();
extern u32 native_fn_ov000_021e4e9c();
extern u32 native_fn_ov000_021e52c0();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x1];
    s8 field_a;
    u8 unknown_b[0x12];
    u8 field_1d;
} Record_native_data_020f6054;
extern Record_native_data_020f6054 native_data_020f6054;
u32 native_main_0203e464(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_020f6054.field_1d == 0) {
        native_data_020f6054.field_1d = 0xAU;
    }
    if (native_data_020f6054.field_1d == 0xA) {
        native_data_020f6054.field_1d = 0x32U;
        if (!(native_fn_ov000_021e4e9c(0x87) == 0)) {
            native_data_020f6054.field_1d = 0x14U;
        } else {
            native_data_020f6054.field_1d = 0x32U;
        }
    }
    if ((native_data_020f6054.field_1d == 0x14) && (native_fn_ov000_021e52c0() != 0)) {
        native_fn_0205bd4c();
        native_data_020f6054.field_1d = 0x32U;
    }
    if ((native_data_020f6054.field_1d == 0x32) && (native_fn_02041800() != 1)) {
        native_data_020f6054.field_1d = 0x37U;
    }
    if (native_data_020f6054.field_1d == 0x37) {
        native_data_020f6054.field_a = 0x1D;
        native_data_020f6054.field_8 = 2;
        native_data_020f6054.field_1d = 0x64U;
    }
    if (native_data_020f6054.field_1d == 0x64) {
        var_r4 = 1;
        native_data_020f6054.field_1d = 0U;
    }
    return var_r4;
}
