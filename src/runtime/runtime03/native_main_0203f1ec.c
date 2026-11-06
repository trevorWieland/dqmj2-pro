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
extern u32 native_fn_020273f0();
extern u32 native_fn_0204076c();
extern u32 native_fn_0205be34();
extern u32 native_fn_0205be4c();
extern u32 native_fn_0205be74();
extern u32 native_fn_0205bea4();
extern u32 native_fn_0205bed4();
extern u32 native_fn_0205bf2c();
extern u32 native_fn_0205c1d0();
extern u32 native_fn_0205c364();
extern u32 native_fn_0205c394();
extern u32 native_fn_ov000_021d8a44();
extern u32 native_fn_ov000_021e07ac();
extern u32 native_fn_ov000_021e07b8();
extern u32 native_fn_ov000_021e07d4();
extern u32 native_fn_ov000_02214fc8();
extern u8 native_data_020f6054[];
u32 native_main_0203f1ec(void) {
    u32 var_r4;

    var_r4 = 1;
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x1C) == 0) {
        native_fn_0205be34(M2C_FIELD(native_data_020f6054, u8 *, 0xC));
        native_fn_ov000_021e07b8(0);
        native_fn_0205be74();
        native_fn_0205bea4(M2C_FIELD((void *) native_fn_ov000_021e07d4(0), s32 *, 4));
        native_fn_0205bed4(M2C_FIELD((void *) native_fn_ov000_021d8a44(), s32 *, 0x4C));
        native_fn_0205be4c(-1);
        native_fn_0205bf2c(1);
        native_fn_0205c364(native_fn_ov000_021e07ac() + 0x178);
        native_fn_0205c394(native_fn_ov000_021e07ac() + 0x184);
        native_fn_ov000_02214fc8(2);
        M2C_FIELD(native_data_020f6054, u8 *, 0x1C) = 0xAU;
    } else if ((M2C_FIELD(native_data_020f6054, u8 *, 0x1C) == 0xA) && (native_fn_020273f0() == 0)) {
        native_fn_0205c1d0(-1);
        var_r4 = native_fn_0204076c();
        M2C_FIELD(native_data_020f6054, u8 *, 0x1C) = 0U;
    }
    return var_r4;
}
