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
extern u32 native_fn_02081f00();
extern u32 native_fn_02081f9c();
extern u8 native_data_021c6e78[];
u32 native_main_020820ac(void) {
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_021c6e78, s8 *, 1) == 0x64) {
        if (native_fn_02081f00() != 0) {
            M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0x6E;
        }
    } else if (M2C_FIELD(native_data_021c6e78, s8 *, 1) != 0x6E) {
        var_r4 = 1;
    } else {
        native_fn_02081f9c();
        M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0;
    }
    return var_r4;
}
