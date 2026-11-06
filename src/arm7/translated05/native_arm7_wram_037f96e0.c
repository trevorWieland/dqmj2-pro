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
extern u32 native_arm7_data_0380fff4;
extern u32 native_arm7_data_04808010;
u32 native_arm7_wram_037f96e0(void) {
    u16 temp_r0;
    u16 temp_r0_2;
    u16 var_r0;
    void *temp_r2;

    M2C_FIELD(&native_arm7_data_04808010, s16 *, 0) = 0x2000;
    temp_r2 = native_arm7_data_0380fff4 + 0x344;
    M2C_FIELD(&native_arm7_data_04808010, s16 *, 0x9C) = 0xD;
    temp_r0_2 = M2C_FIELD(temp_r2, u16 *, 0x1A);
    if (temp_r0_2 == 1) {
        M2C_FIELD(temp_r2, u16 *, 0x1A) = 2U;
        return 2U;
    }
    if (temp_r0_2 == 2) {
        M2C_FIELD(temp_r2, u16 *, 0x1A) = 0U;
        return 0U;
    }
    temp_r0 = M2C_FIELD(temp_r2, u16 *, 0xC);
    if (temp_r0 != 2) {
        return (u32) temp_r0;
    }
    var_r0 = M2C_FIELD(temp_r2, u16 *, 8);
    if (var_r0 != 0x40) {
        var_r0 = 0;
        M2C_FIELD(&native_arm7_data_04808010, s16 *, 0x38) = 0;
    }
    return (u32) var_r0;
}
