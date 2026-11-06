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
extern u32 native_arm7_fn_03802824(u32, u32, u32, u32);
extern u32 native_arm7_fn_03802a0c(u32, u32, u32, u32);
extern u32 native_arm7_fn_03802860(u32, u32, u32, u32);
extern u32 native_arm7_data_038090c0;
extern u32 native_arm7_data_038096c0;
extern u32 native_arm7_data_03802974;
u32 native_arm7_wram_03802ce0(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r3;
    u32 temp_r4;
    u32 var_r0;

    var_r0 = native_arm7_fn_03802824(arg0, arg1, arg2, arg3);
    if (var_r0 != 0) {
        temp_r4 = native_arm7_data_038090c0;
        M2C_FIELD(&native_arm7_data_038096c0, u32 *, 0x10) = 1U;
        temp_r3 = M2C_FIELD(temp_r4, s32 *, 0x28) + 1 + arg2;
        M2C_FIELD(&native_arm7_data_038096c0, u32 *, 4) = temp_r3;
        native_arm7_fn_03802a0c(arg0, 3U, (u32) &native_arm7_data_038096c0, temp_r3);
        native_arm7_fn_03802860(arg1, 0U, arg2, (u32) &native_arm7_data_03802974);
        var_r0 = M2C_FIELD(temp_r4, u32 *, 0);
        if (var_r0 == 0) {
            var_r0 = M2C_FIELD(&native_arm7_data_038096c0, u32 *, 0x10);
            if (var_r0 == 0) {
                var_r0 = 1;
                M2C_FIELD(temp_r4, u32 *, 0) = 1U;
            }
        }
    }
    return var_r0;
}
