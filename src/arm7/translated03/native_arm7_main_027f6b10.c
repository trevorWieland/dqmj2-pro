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
u32 native_arm7_main_027f6b10(u32 arg0) {
    native_arm7_fn_037fe5a8(0x8000U);
    return native_arm7_fn_027f6ec0(0x86U, 0U, arg0, 1U);
}
