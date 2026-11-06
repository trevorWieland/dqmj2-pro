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
extern u32 native_arm7_fn_027ebb50(u32);
extern u32 native_arm7_fn_037f8988(u32, u32, u32);
extern u32 native_arm7_fn_027f0484(u32, u32);
extern u32 native_arm7_fn_027efec8(u32, u32);
extern u32 native_arm7_fn_027eff00(u32);
extern u32 native_arm7_fn_027ec1d4(u32);
extern u32 native_arm7_data_0380fff4;
extern u8 native_arm7_data_048080ac;
void native_arm7_main_027f09b8(void *arg0, s32 arg1) {
    void *temp_r4;

    temp_r4 = native_arm7_data_0380fff4 + 0x17C;
    M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x550) = (s32) (M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x550) + 1);
    if (((u32) (M2C_FIELD(arg0, u16 *, 0x14) << 0x1C) >> 0x1E) == 0) {
        native_arm7_fn_027ebb50((u32) arg0);
        native_arm7_fn_037f8988(temp_r4 + 0x30, temp_r4 + 0x24, arg0 - 0x10);
        native_arm7_fn_027f0484((u32) arg0, 0U);
    } else {
        native_arm7_fn_027efec8(temp_r4 + 0x30, arg0 - 0x10);
    }
    M2C_FIELD(native_arm7_data_0380fff4, s16 *, 0x454) = 0;
    if (((u32) (M2C_FIELD(M2C_FIELD(native_arm7_data_0380fff4, void **, 0x45C), u16 *, 0xC) << 0x12) >> 0x1F) == 0) {
        M2C_FIELD((u32) &native_arm7_data_048080ac, s16 *, 0) = 8;
        M2C_FIELD((u32) &native_arm7_data_048080ac, s16 *, 2) = 5;
        if (arg1 != 0) {
            if (M2C_FIELD(temp_r4, u16 *, 0x2C) != 0) {
                native_arm7_fn_027eff00(1U);
            }
            if (M2C_FIELD(temp_r4, u16 *, 0x20) != 0) {
                native_arm7_fn_027eff00(0U);
            }
        }
    }
    if (M2C_FIELD(temp_r4, u16 *, 0x38) != 0) {
        if (arg1 != 0) {
            native_arm7_fn_027eff00(2U);
        }
    } else {
        native_arm7_fn_027ec1d4(0U);
    }
}
