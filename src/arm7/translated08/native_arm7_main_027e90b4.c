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
extern u32 native_arm7_fn_037fdf9c(u32, u32, u32);
extern u32 native_arm7_data_04805f80;
extern u32 native_arm7_data_04805fa0;
extern u32 native_arm7_data_04805fc0;
extern u32 native_arm7_data_04805fe0;
u32 native_arm7_main_027e90b4(u32 arg0) {
    native_arm7_fn_037fdf9c(arg0, (u32) &native_arm7_data_04805f80, 0x14U);
    native_arm7_fn_037fdf9c(arg0 + 0x14, (u32) &native_arm7_data_04805fa0, 0x14U);
    native_arm7_fn_037fdf9c(arg0 + 0x28, (u32) &native_arm7_data_04805fc0, 0x14U);
    native_arm7_fn_037fdf9c(arg0 + 0x3C, (u32) &native_arm7_data_04805fe0, 0x14U);
    return 0U;
}
