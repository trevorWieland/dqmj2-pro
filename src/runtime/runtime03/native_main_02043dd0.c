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
extern u32 native_fn_02043a24();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_ov001_021e3168();
extern u8 native_data_020f69c4[];
u32 native_main_02043dd0(void) {
    if ((M2C_FIELD(native_data_020f69c4, u8 *, 7) == 0) && (native_fn_ov001_021e3168() != 0)) {
        M2C_FIELD(native_data_020f69c4, u8 *, 7) = 1U;
    }
    if ((M2C_FIELD(native_data_020f69c4, u8 *, 6) == 0) && (native_fn_02043a24() != 0)) {
        M2C_FIELD(native_data_020f69c4, u8 *, 6) = 1U;
    }
    if ((M2C_FIELD(native_data_020f69c4, u8 *, 7) != 0) && (M2C_FIELD(native_data_020f69c4, u8 *, 6) != 0)) {
        M2C_FIELD(native_data_020f69c4, u8 *, 7) = 0U;
        M2C_FIELD(native_data_020f69c4, u8 *, 6) = 0U;
        M2C_FIELD(native_data_020f69c4, s8 *, 3) = 7;
    }
    native_fn_0204437c();
    native_fn_0204439c();
    return 0U;
}
