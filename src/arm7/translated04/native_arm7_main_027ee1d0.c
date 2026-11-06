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
extern u32 native_arm7_fn_027e8e68(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ee1d0(s32 arg0, void *arg1) {
    u32 var_r3;

    var_r3 = 1;
    M2C_FIELD(arg1, s16 *, 2) = 1;
    if (M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x34C) == 0x10) {
        var_r3 = native_arm7_fn_027e8e68(arg0 + 0x10);
    }
    return var_r3;
}
