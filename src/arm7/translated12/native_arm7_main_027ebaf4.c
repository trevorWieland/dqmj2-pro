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
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_027ec118(u32);
extern u32 native_arm7_fn_037f8988(u32, u32, u32);
extern u32 native_arm7_fn_037fb8f0(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ebaf4(u32 arg0, u32 arg1) {
    void *temp_r4;
    u32 temp_r5;

    temp_r4 = native_arm7_data_0380fff4 + 0x1AC;
    temp_r5 = native_arm7_fn_037fb928(0x01000000U);
    if (M2C_FIELD(temp_r4, u16 *, 8) == 0) {
        native_arm7_fn_027ec118(0U);
    }
    native_arm7_fn_037f8988(arg0, (u32) temp_r4, arg1);
    return native_arm7_fn_037fb8f0(temp_r5);
}
