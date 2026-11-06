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
extern u32 native_arm7_fn_037fdf74(u32, u32, u32);
extern u32 native_arm7_fn_027ea584(void);
extern u32 native_arm7_fn_027ea13c(u32, u32, u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027f1fb4(u32 arg0, u32 arg1) {
    native_arm7_fn_037fdf74(0U, arg0, 0x2CU);
    M2C_FIELD(arg0, s16 *, 0x10) = (s16) native_arm7_fn_027ea584();
    return native_arm7_fn_027ea13c(arg0 + 0x18, arg1, native_arm7_data_0380fff4 + 0x324, native_arm7_data_0380fff4 + 0x3A8);
}
