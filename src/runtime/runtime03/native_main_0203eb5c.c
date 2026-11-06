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
extern u32 native_fn_02040434();
extern u32 native_fn_02041510();
extern u32 native_fn_02041538();
extern u32 native_fn_02041800();
extern u32 native_fn_02041814();
extern u32 native_fn_020418b0();
extern u32 native_fn_02041944();
extern u32 native_fn_ov000_021da16c();
extern u32 native_fn_ov000_021e0764();
extern u32 native_fn_ov000_021e0d78();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e7940();
extern u8 native_data_020f6054[];
u32 native_main_0203eb5c(void) {
    u32 var_r4;

    var_r4 = 0;
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x14) == 0) && (native_fn_02041814() == 2)) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x14) = 0xAU;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x14) == 0xA) {
        native_fn_ov000_021e0d78(1, 0, 1);
        native_fn_02041510(1, 2, 0x1E);
        if ((s32) native_fn_02041944() > -0xF) {
            native_fn_02041538(1, 2, 0x1E);
        } else {
            native_fn_020418b0(2);
        }
        native_fn_ov000_021e7940(0x1E);
        M2C_FIELD(native_data_020f6054, u8 *, 0x14) = 0x14U;
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x14) == 0x14) && (native_fn_02041800() != 1)) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x14) = 0x1EU;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x14) == 0x1E) {
        native_fn_ov000_021e7940(0);
        M2C_FIELD(native_data_020f6054, s8 *, 8) = 6;
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x1D;
        M2C_FIELD(native_data_020f6054, u8 *, 0x14) = 0U;
        var_r4 = 1;
    }
    native_fn_ov000_021e0764();
    native_fn_ov000_021e1894(0);
    native_fn_ov000_021da16c();
    native_fn_02040434();
    return var_r4;
}
