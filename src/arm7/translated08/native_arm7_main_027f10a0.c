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
extern u32 native_arm7_fn_027eb90c(u32);
extern u32 native_arm7_fn_027ebb50(u32);
extern u32 native_arm7_fn_037f8988(u32, u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027f10a0(void *arg0) {
    M2C_FIELD(arg0, u16 *, 2) = (u16) native_arm7_fn_027eb90c(arg0 + 0x18);
    if (M2C_FIELD(arg0, u16 *, 2) == 0xFF) {
        M2C_FIELD(arg0, u16 *, 2) = 0U;
    }
    M2C_FIELD(arg0, s16 *, 4) = (s16) M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x3EC);
    if (M2C_FIELD(arg0, u16 *, 0x14) & 0x4000) {
        M2C_FIELD(arg0, u16 *, 0x12) = (u16) (M2C_FIELD(arg0, u16 *, 0x12) + 8);
    }
    native_arm7_fn_027ebb50((u32) arg0);
    return native_arm7_fn_037f8988(native_arm7_data_0380fff4 + 0x188, native_arm7_data_0380fff4 + 0x1A0, arg0 - 0x10);
}
