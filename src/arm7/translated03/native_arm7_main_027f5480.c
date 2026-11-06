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
extern u32 native_arm7_fn_027f5554(u32);
u32 native_arm7_main_027f5480(void) {
    u16 sp0;

    native_arm7_fn_027f5554((u32) &sp0);
    if (sp0 & 1) {
        return 0U;
    }
    if (sp0 & 2) {
        return 1U;
    }
    return 0U;
}
