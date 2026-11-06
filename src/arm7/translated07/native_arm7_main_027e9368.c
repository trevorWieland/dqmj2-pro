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
extern u32 native_arm7_fn_027ea5fc(u32, u32);
u32 native_arm7_main_027e9368(u32 arg0, u32 arg1) {
    if (arg0 > 3U) {
        return 5U;
    }
    if (arg1 > 0x3FU) {
        return 5U;
    }
    native_arm7_fn_027ea5fc(0x13U, arg0);
    native_arm7_fn_027ea5fc(0x35U, arg1);
    return 0U;
}
