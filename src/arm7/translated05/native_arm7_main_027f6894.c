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
extern u32 native_arm7_fn_037fe5a8(u32);
extern u32 native_arm7_fn_027f6ec0(u32, u32, u32, u32);
u32 native_arm7_main_027f6894(u32 arg0) {
    u16 sp0;

    native_arm7_fn_037fe5a8(0x8000U);
    native_arm7_fn_027f6ec0(0x86U, 0x40U, (u32) &sp0, 1U);
    if ((((u32) (sp0 << 0x1C) >> 0x1C) & 0xB) != 1) {
        return 0U;
    }
    native_arm7_fn_027f6ec0(0x86U, 0x10U, arg0, 1U);
    return 1U;
}
