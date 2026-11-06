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
extern u32 native_arm7_fn_027ec1d4(u32);
extern u32 native_arm7_fn_027ec0d8(u32);
extern u32 native_arm7_fn_027e9ea0(void);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027ebf6c(u32 arg0) {
    u32 temp_r4;
    u32 var_r0;

    temp_r4 = native_arm7_data_0380fff4;
    native_arm7_fn_027ec1d4(arg0);
    var_r0 = native_arm7_fn_027ec0d8(arg0);
    if (var_r0 != 0) {
        M2C_FIELD(((arg0 * 0x1C) + M2C_FIELD(native_arm7_data_0380fff4, s32 *, 0x31C)), s16 *, 2) = 0;
        M2C_FIELD(temp_r4, u16 *, 0x53A) = (u16) (M2C_FIELD(temp_r4, u16 *, 0x53A) & ~(1 << var_r0));
        M2C_FIELD(temp_r4, u16 *, 0x538) = (u16) (M2C_FIELD(temp_r4, u16 *, 0x538) - 1);
        var_r0 = (u32) M2C_FIELD(temp_r4, u16 *, 0x538);
        if (var_r0 == 0) {
            var_r0 = native_arm7_fn_027e9ea0();
        }
    }
    return var_r0;
}
