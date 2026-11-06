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
extern u32 native_arm7_fn_03802824(void);
extern u32 native_arm7_fn_038029d8(void);
extern u32 native_arm7_fn_03802860(u32, u32, u32, u32);
extern u32 native_arm7_fn_0380272c(u32, u32);
extern u32 native_arm7_data_038090c0;
extern u32 native_arm7_data_038096c0;
extern u32 native_arm7_data_03807278;
extern u32 native_arm7_data_03802924;
u32 native_arm7_wram_03802ea8(void) {
    u32 temp_r4;
    u32 var_r0;

    var_r0 = native_arm7_fn_03802824();
    if (var_r0 != 0) {
        temp_r4 = native_arm7_data_038090c0;
        native_arm7_fn_038029d8();
        M2C_FIELD(&native_arm7_data_038096c0, s32 *, 4) = 1;
        native_arm7_fn_03802860((u32) &native_arm7_data_03807278, 0U, 1U, (u32) &native_arm7_data_03802924);
        var_r0 = native_arm7_fn_0380272c(M2C_FIELD(temp_r4, u32 *, 0x38), M2C_FIELD(temp_r4, u32 *, 0x3C));
    }
    return var_r0;
}
