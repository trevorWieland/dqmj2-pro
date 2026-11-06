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
extern u32 native_arm7_fn_037fdf9c(u32, u32, u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027e9f1c(u32 arg0, u32 arg1) {
    void *temp_r4;

    temp_r4 = native_arm7_data_0380fff4 + 0x344;
    if (arg0 > 0x80U) {
        return 4U;
    }
    native_arm7_fn_037fdf9c(arg1, M2C_FIELD(temp_r4, u32 *, 0x9C), arg0 + 1);
    M2C_FIELD(temp_r4, s16 *, 0xA0) = (s16) arg0;
    return 0U;
}
