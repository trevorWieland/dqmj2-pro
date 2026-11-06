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
extern u32 native_arm7_fn_027e05d8(u32);
extern u32 native_arm7_data_027f7884;
u32 native_arm7_main_027e059c(void) {
    s32 var_r2;
    u32 var_r3;
    u8 temp_r0;

    var_r3 = 0;
    var_r2 = 0;
    do {
        temp_r0 = M2C_FIELD(((u32) &native_arm7_data_027f7884 + var_r2), u8 *, 0x1554);
        var_r2 += 1;
        var_r3 += temp_r0;
    } while (var_r2 < 0x20);
    return native_arm7_fn_027e05d8(var_r3 >> 5);
}
