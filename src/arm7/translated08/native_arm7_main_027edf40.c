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
extern u32 native_arm7_fn_037f8d58(u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027edf40(void) {
    u32 temp_r0;

    temp_r0 = native_arm7_fn_037f886c(native_arm7_data_0380fff4 + 0x188, 0x10U);
    if (temp_r0 == 0) {
        native_arm7_fn_027eb078(1U);
        return 0U;
    }
    M2C_FIELD(temp_r0, s16 *, 0xC) = 0x8C;
    M2C_FIELD(temp_r0, s16 *, 0xE) = 0;
    native_arm7_fn_037f8d58(native_arm7_data_0380fff4 + 0x188, temp_r0);
    return 1U;
}
