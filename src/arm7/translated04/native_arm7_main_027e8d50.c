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
extern u32 native_arm7_fn_027e8da8(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027e8d50(void) {
    u32 temp_r4;

    temp_r4 = native_arm7_data_0380fff4;
    native_arm7_fn_027e8da8(temp_r4 + 0x194);
    native_arm7_fn_027e8da8(temp_r4 + 0x1A0);
    native_arm7_fn_027e8da8(temp_r4 + 0x1AC);
    native_arm7_fn_027e8da8(temp_r4 + 0x1B8);
    native_arm7_fn_027e8da8(temp_r4 + 0x1C4);
    native_arm7_fn_027e8da8(temp_r4 + 0x1D0);
    native_arm7_fn_027e8da8(temp_r4 + 0x1DC);
    return native_arm7_fn_027e8da8(temp_r4 + 0x1E8);
}
