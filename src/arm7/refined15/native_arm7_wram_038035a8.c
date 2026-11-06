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
extern u32 native_arm7_fn_038035f0(void);
extern u32 native_arm7_fn_03803690(void);
extern u32 native_arm7_data_03809920;
extern u8 native_arm7_data_027ffe1f;
u32 native_arm7_wram_038035a8(void) {
    if (M2C_FIELD(&native_arm7_data_03809920, u32 *, 0xC) == 0) {
        if (native_arm7_data_027ffe1f & 0x80) {
            native_arm7_fn_038035f0();
        } else {
            native_arm7_fn_03803690();
        }
    }
    return M2C_FIELD(&native_arm7_data_03809920, u32 *, 0xC);
}
