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
extern u32 native_arm7_fn_027ea0ec(u32, u32);
extern u32 native_arm7_data_0380fff4;
extern u32 native_arm7_data_04808018;
u32 native_arm7_main_027e8e68(u16 *arg0) {
    if (*arg0 & 1) {
        return 5U;
    }
    native_arm7_fn_027ea0ec(native_arm7_data_0380fff4 + 0x324, (u32) arg0);
    native_arm7_fn_027ea0ec((u32) &native_arm7_data_04808018, (u32) arg0);
    M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x340) = (s32) (M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x340) | 2);
    return 0U;
}
