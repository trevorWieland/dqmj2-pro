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
extern u32 native_arm7_fn_037fca58(u32);
extern u32 native_arm7_data_0380786c;
u32 native_arm7_wram_037fca1c(void) {
    u32 var_r0;

    var_r0 = native_arm7_data_0380786c;
    if (var_r0 == 0) {
        native_arm7_data_0380786c = 1;
        native_arm7_fn_037fca58(1U);
        native_arm7_fn_037fca58(7U);
        var_r0 = native_arm7_fn_037fca58(8U);
    }
    return var_r0;
}
