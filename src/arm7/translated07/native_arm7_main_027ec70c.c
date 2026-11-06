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
extern u32 native_arm7_fn_037f9198(void);
extern u32 native_arm7_fn_027ea188(void);
u32 native_arm7_main_027ec70c(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 2) = 1;
    if ((u32) M2C_FIELD(arg0, u16 *, 0x10) > 1U) {
        return 5U;
    }
    native_arm7_fn_037f9198();
    if (M2C_FIELD(arg0, u16 *, 0x10) == 1) {
        native_arm7_fn_027ea188();
    }
    return 0U;
}
