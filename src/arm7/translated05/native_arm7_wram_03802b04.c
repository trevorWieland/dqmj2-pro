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
extern u32 native_arm7_data_038028e4;
u32 native_arm7_wram_03802b04(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r3;
    u32 var_r0;

    var_r0 = native_arm7_fn_03802824(arg0, arg1, arg2, arg3);
    if (var_r0 != 0) {
        temp_r3 = M2C_FIELD(native_arm7_data_038090c0, s32 *, 0x28) + 1 + arg2;
        M2C_FIELD(&native_arm7_data_038096c0, u32 *, 4) = temp_r3;
        native_arm7_fn_03802a0c(arg0, 3U, (u32) &native_arm7_data_038096c0, temp_r3);
        var_r0 = native_arm7_fn_03802860(0U, arg1, arg2, (u32) &native_arm7_data_038028e4);
    }
    return var_r0;
}
