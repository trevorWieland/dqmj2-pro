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
extern u32 native_arm7_fn_0380398c(u32);
extern u32 native_arm7_fn_027f4ddc(void);
extern u32 native_arm7_fn_027f55c4(u32, u32, u32);
extern u32 native_arm7_fn_038039e8(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027f4e7c(u32 arg0, u32 arg1, u32 arg2) {
    native_arm7_fn_0380398c(M2C_FIELD(native_arm7_data_0380fff4, u32 *, 0x314));
    native_arm7_fn_027f4ddc();
    native_arm7_fn_027f55c4(arg0, arg1, arg2);
    return native_arm7_fn_038039e8(M2C_FIELD(native_arm7_data_0380fff4, u32 *, 0x314));
}
