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
extern u32 native_fn_020273f0();
extern u8 native_data_020f6054[];
u32 native_main_0203ecf4(void) {
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x12) == 0) {
        if ((native_fn_020273f0() == 0) || (native_fn_020273f0() == 0xC)) {
            M2C_FIELD(native_data_020f6054, u8 *, 0x12) = 0xAU;
        }
    } else {
        M2C_FIELD(native_data_020f6054, u8 *, 0x12) = 0U;
        M2C_FIELD(native_data_020f6054, s8 *, 8) = 0;
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x1D;
        var_r4 = 1;
    }
    return var_r4;
}
