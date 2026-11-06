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
extern u32 native_arm7_fn_027e72d4(u32);
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e6348(void *arg0) {
    void *var_r0;

    var_r0 = arg0;
    if (*M2C_FIELD(&native_arm7_data_027f8884, u16 **, 0x550) == 9) {
        var_r0 = (void *) native_arm7_fn_027e72d4((u32) (u16) M2C_FIELD(var_r0, s32 *, 4));
    }
    return (u32) var_r0;
}
