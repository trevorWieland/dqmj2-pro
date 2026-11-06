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
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_data_038076f0;
u32 native_arm7_wram_037fc590(void) {
    u32 temp_r0;
    u32 temp_r3;
    u32 var_r4;

    temp_r0 = native_arm7_fn_037fdd00();
    var_r4 = 0;
    temp_r3 = M2C_FIELD(&native_arm7_data_038076f0, u32 *, 4);
    if (temp_r3 != 0) {
        M2C_FIELD(&native_arm7_data_038076f0, u32 *, 4) = (u32) (temp_r3 - 1);
        var_r4 = temp_r3;
    }
    native_arm7_fn_037fdd14(temp_r0);
    return var_r4;
}
