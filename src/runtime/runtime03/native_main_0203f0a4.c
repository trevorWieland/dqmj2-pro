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
extern u32 native_fn_020282a8();
extern u32 native_fn_0205be14();
extern u32 native_fn_0205be34();
extern u32 native_fn_0205bf1c();
extern u32 native_fn_ov000_021d8a08();
extern u32 native_fn_ov000_021e316c();
extern u32 native_fn_ov000_02210f64();
extern u32 native_fn_ov000_022189e4();
extern u32 native_fn_ov000_02218b4c();
extern u32 native_fn_ov000_02218b60();
extern u32 native_fn_ov000_02219404();
extern u8 native_data_020f6054[];
u32 native_main_0203f0a4(void) {
    u8 temp_r4;

    native_fn_ov000_021e316c();
    temp_r4 = M2C_FIELD(native_data_020f6054, u8 *, 0xC);
    native_fn_0205be34(temp_r4);
    M2C_FIELD(native_data_020f6054, u8 *, 0xC) = (u8) native_fn_0205be14();
    M2C_FIELD(native_data_020f6054, s8 *, 4) = (s8) native_fn_0205bf1c();
    native_fn_ov000_021d8a08(0);
    native_fn_020282a8(0, 0x1E000);
    native_fn_ov000_02210f64(0);
    if (native_fn_ov000_022189e4(temp_r4, M2C_FIELD(native_data_020f6054, u8 *, 0xC)) != 0) {
        native_fn_ov000_02218b4c();
    }
    native_fn_ov000_02219404(M2C_FIELD(native_data_020f6054, u8 *, 0xC));
    native_fn_ov000_02218b60();
    M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 1;
    return (u32) native_data_020f6054;
}
