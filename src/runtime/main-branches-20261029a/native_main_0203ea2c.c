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
extern u32 native_fn_0205d53c();
extern u32 native_fn_ov000_021d8958();
extern u32 native_fn_ov000_021da16c();
extern u32 native_fn_ov000_021e0764();
extern u32 native_fn_ov000_021e0d78();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e4e9c();
extern u32 native_fn_ov000_021e52c0();
extern u32 native_fn_ov000_02211960();
extern u32 native_fn_ov000_0221310c();
extern u32 native_fn_ov000_02219e04();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x6];
    s8 field_11;
    u8 unknown_12[0x5];
    u8 field_17;
} Record_native_data_020f6054;
extern Record_native_data_020f6054 native_data_020f6054;
u32 native_main_0203ea2c(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_020f6054.field_17 == 0) {
        native_fn_ov000_021e0d78(1, 0, 1);
        if (!(native_fn_ov000_021e4e9c(0x88) == 0)) {
            native_data_020f6054.field_17 = 0xAU;
        } else {
            native_data_020f6054.field_17 = 0x3CU;
        }
    }
    if ((native_data_020f6054.field_17 == 0xA) && (native_fn_ov000_021e52c0() != 0)) {
        var_r4 = 1;
        native_data_020f6054.field_a = (s8) native_data_020f6054.field_11;
        native_data_020f6054.field_17 = 0U;
    }
    if (native_data_020f6054.field_17 == 0x3C) {
        native_data_020f6054.field_a = 5;
        native_data_020f6054.field_17 = 0x64U;
    }
    if (native_data_020f6054.field_17 == 0x64) {
        native_data_020f6054.field_17 = 0U;
        var_r4 = 1;
    }
    native_fn_ov000_02219e04();
    native_fn_ov000_021d8958();
    if ((u32) native_data_020f6054.field_17 <= 0x1EU) {
        native_fn_ov000_021e1894(0);
        native_fn_ov000_021e0764();
        native_fn_0205d53c();
        native_fn_ov000_0221310c();
        native_fn_ov000_02211960(0);
        native_fn_ov000_021da16c();
    }
    native_fn_02040434();
    return var_r4;
}
