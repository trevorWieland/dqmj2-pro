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
extern u32 native_arm7_fn_027f6f1c(void);
extern u32 native_arm7_fn_027f6f90(u32, u32);
extern u32 native_arm7_fn_027f7010(u32, u32);
extern u32 native_arm7_fn_027f6f5c(void);
u32 native_arm7_main_027f67cc(u32 arg0) {
    native_arm7_fn_037fe5a8(0x8000U);
    native_arm7_fn_027f6f1c();
    native_arm7_fn_027f6f90(6U, 0x20U);
    native_arm7_fn_027f7010(arg0, 7U);
    return native_arm7_fn_027f6f5c();
}
