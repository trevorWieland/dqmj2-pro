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
extern u32 native_fn_0203e660();
extern u32 native_fn_02040434();
extern u32 native_fn_020404f0();
extern u32 native_fn_0204071c();
extern u32 native_fn_0205bdfc();
extern u32 native_fn_0205be14();
extern u32 native_fn_0205be4c();
extern u32 native_fn_0205bf04();
extern u32 native_fn_0205bf2c();
extern u32 native_fn_0205d53c();
extern u32 native_fn_0205f35c();
extern u32 native_fn_ov000_021d8958();
extern u32 native_fn_ov000_021d8c80();
extern u32 ov000_saved_world_position_get_021e07b8();
extern u32 native_fn_ov000_021e0d78();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e339c();
extern u32 native_fn_ov000_021e74e8();
extern u32 native_fn_ov000_021e7510();
extern u32 native_fn_ov000_02219404();
extern u8 native_data_020f6054[];
u32 native_main_0203f4b0(void) {
    if (M2C_FIELD(native_data_020f6054, u8 *, 9) != 0) {
        goto block_2;
    }
    native_fn_0204071c(0);
    native_fn_ov000_021e0d78(1, 0, 1);
    native_fn_ov000_021e339c();
    native_fn_ov000_021d8c80(1);
    native_fn_ov000_021e74e8(1);
    ov000_saved_world_position_get_021e07b8(0);
    native_fn_ov000_021e7510();
    native_fn_0205bdfc(M2C_FIELD(native_data_020f6054, u8 *, 0x2B));
    native_fn_0205f35c(-1, 0x9F);
    M2C_FIELD(native_data_020f6054, u8 *, 9) = 0xAU;
    goto block_7;
block_2:
    if (M2C_FIELD(native_data_020f6054, u8 *, 9) != 0xA) {
        goto block_5;
    }
    if (native_fn_0203e660(2, 0) == 0) {
        goto block_7;
    }
    M2C_FIELD(native_data_020f6054, u8 *, 9) = 0x64U;
    goto block_7;
block_5:
    if (M2C_FIELD(native_data_020f6054, u8 *, 9) != 0x64) {
        goto block_7;
    }
    native_fn_0205bf2c(6);
    native_fn_0205bf04(0);
    native_fn_0205be4c(-1);
    native_fn_0205be14();
    native_fn_ov000_02219404();
    native_fn_020404f0(0x1D);
    M2C_FIELD(native_data_020f6054, s8 *, 8) = 0xC;
    M2C_FIELD(native_data_020f6054, u8 *, 9) = 0U;
block_7:
    native_fn_ov000_021e1894(0);
    native_fn_ov000_021d8958();
    native_fn_0205d53c();
    native_fn_02040434();
    return 0U;
}
