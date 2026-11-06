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
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u8 native_data_020f6054[];
u32 native_main_0203ef34(void) {
    u32 temp_r0;

    if (M2C_FIELD(native_data_020f6054, u32 *, 0x40) == 0) {
        native_fn_02041510(1, 2, 0xA);
        M2C_FIELD(native_data_020f6054, u32 *, 0x40) = 0xAU;
        return (u32) native_data_020f6054;
    }
    if (M2C_FIELD(native_data_020f6054, u32 *, 0x40) != 0xA) {
        return M2C_FIELD(native_data_020f6054, u32 *, 0x40);
    }
    temp_r0 = native_fn_02041800();
    if (temp_r0 == 1) {
        return temp_r0;
    }
    M2C_FIELD(native_data_020f6054, s8 *, 8) = 5;
    M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x1D;
    M2C_FIELD(native_data_020f6054, u32 *, 0x40) = 0U;
    return (u32) native_data_020f6054;
}
