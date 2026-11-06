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
extern u32 native_fn_02041800();
extern u32 native_fn_02041814();
extern u32 native_fn_0205c1f8();
extern u32 native_fn_0205f35c();
extern u32 native_fn_ov000_021e1894();
extern u8 native_data_020f6054[];
u32 native_main_0203f864(void) {
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0) {
        native_fn_0205f35c(-1, 0x9B);
        native_fn_02041510(1, 3, 0xF);
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0xAU;
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0xA) && (native_fn_02041800() != 1)) {
        native_fn_02041510(0, 3, 0x1E);
        native_fn_0205c1f8(1);
        native_fn_ov000_021e1894(0);
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0x14U;
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0x14) && (native_fn_02041800() != 1)) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0x1EU;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0x1E) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0x64U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0x64) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0x6EU;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0x6E) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0x78U;
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0x78) && (native_fn_02041814() != 1)) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0xC8U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x10) == 0xC8) {
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 5;
        M2C_FIELD(native_data_020f6054, u8 *, 0x10) = 0U;
        var_r4 = 1;
    }
    native_fn_02040434();
    return var_r4;
}
