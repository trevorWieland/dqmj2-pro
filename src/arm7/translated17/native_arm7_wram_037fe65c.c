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
extern u32 native_arm7_fn_037fe5a8(u32);
extern u16 native_arm7_data_04000136;
extern u16 native_arm7_data_027fffa8;
u32 native_arm7_wram_037fe65c(void) {
    s32 var_r4;

    var_r4 = 0;
    native_arm7_fn_037fe5a8(0x8000U);
    if (native_arm7_data_04000136 & 0x80) {
        var_r4 = 0x8000;
    }
    native_arm7_data_027fffa8 = var_r4 | ((native_arm7_data_04000136 & 0xB) << 0xA);
    return (u32) (u32) &native_arm7_data_027fffa8;
}
