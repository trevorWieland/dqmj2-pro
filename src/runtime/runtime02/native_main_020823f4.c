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
extern u32 native_fn_0203cfe0();
extern u32 native_fn_02082108();
extern u32 native_fn_020822ac();
extern u8 native_data_021c6e78[];
u32 native_main_020823f4(void) {
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_021c6e78, s8 *, 1) == 0) {
        native_fn_0203cfe0();
        native_fn_02082108();
        M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0xA;
    } else if (M2C_FIELD(native_data_021c6e78, s8 *, 1) == 0xA) {
        if (native_fn_020822ac() != 0) {
            M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0x64;
        }
    } else {
        var_r4 = 1;
    }
    return var_r4;
}
