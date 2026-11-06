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
extern u32 native_arm7_fn_027f0ce0(u32);
extern u32 native_arm7_fn_037f8598(u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_wram_037fa598(void) {
    void *temp_r4;
    s32 var_r5;

    var_r5 = 0;
    temp_r4 = native_arm7_data_0380fff4 + 0x42C;
    native_arm7_fn_027f0ce0(2U);
    native_arm7_fn_027f0ce0(1U);
    native_arm7_fn_027f0ce0(0U);
    if (M2C_FIELD(temp_r4, u16 *, 0x28) != 0) {
        if (*M2C_FIELD(temp_r4, u16 **, 0x30) != 0) {
            var_r5 = 1;
        } else {
            M2C_FIELD(temp_r4, u16 *, 0x28) = 0U;
        }
    }
    if (M2C_FIELD(temp_r4, u16 *, 0x14) != 0) {
        if (*M2C_FIELD(temp_r4, u16 **, 0x1C) == 0) {
            M2C_FIELD(temp_r4, u16 *, 0x14) = 0U;
        } else {
            var_r5 = 1;
        }
    }
    if (M2C_FIELD(temp_r4, u16 *, 0) != 0) {
        if (*M2C_FIELD(temp_r4, u16 **, 8) == 0) {
            M2C_FIELD(temp_r4, u16 *, 0) = 0U;
        } else {
            var_r5 = 1;
        }
    }
    if (var_r5 != 0) {
        native_arm7_fn_037f8598(0U, 0xEU);
    }
    return native_arm7_fn_037f8598(0U, 0x14U);
}
