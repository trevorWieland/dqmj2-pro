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
extern u32 native_arm7_fn_027ea1b8(void);
extern u32 native_arm7_fn_037fdfd0(u32, u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ea188(void) {
    native_arm7_fn_027ea1b8();
    return native_arm7_fn_037fdfd0(0U, native_arm7_data_0380fff4 + 0x53C, 0xB4U);
}
