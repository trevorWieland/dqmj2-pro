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
extern u32 native_arm7_fn_027eb8ec(void);
extern u32 native_arm7_fn_037f8908(u32, u32);
extern u32 native_arm7_fn_037fc15c(void);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027eb1dc(void) {
    u32 temp_r4;

    temp_r4 = native_arm7_data_0380fff4;
    native_arm7_fn_027eb8ec();
    native_arm7_fn_037f8908(temp_r4 + 0x188, M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x318) - 0xC);
    native_arm7_fn_037f8908(temp_r4 + 0x188, M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x3E0) - 0xC);
    return native_arm7_fn_037fc15c();
}
