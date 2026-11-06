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
extern u32 native_arm7_fn_027f10a0(u32);
extern u32 native_arm7_fn_027eff00(u32);
u32 native_arm7_main_027f1088(u32 arg0) {
    native_arm7_fn_027f10a0(arg0);
    return native_arm7_fn_027eff00(1U);
}
