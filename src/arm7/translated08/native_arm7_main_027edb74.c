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
extern u32 native_arm7_fn_037f886c(u32, u32);
extern u32 native_arm7_fn_027eb078(u32);
extern u32 native_arm7_fn_027ea0ec(u32, u32);
extern u32 native_arm7_fn_037f8d58(u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027edb74(u32 arg0, s16 arg1) {
    u32 temp_r0;

    temp_r0 = native_arm7_fn_037f886c(native_arm7_data_0380fff4 + 0x188, 0x18U);
    if (temp_r0 == 0) {
        native_arm7_fn_027eb078(1U);
        return 0U;
    }
    M2C_FIELD(temp_r0, s16 *, 0xC) = 0x84;
    M2C_FIELD(temp_r0, s16 *, 0xE) = 4;
    native_arm7_fn_027ea0ec(temp_r0 + 0x10, arg0);
    M2C_FIELD(temp_r0, s16 *, 0x16) = arg1;
    native_arm7_fn_037f8d58(native_arm7_data_0380fff4 + 0x188, temp_r0);
    return 1U;
}
