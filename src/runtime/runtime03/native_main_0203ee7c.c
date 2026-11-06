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
extern u32 native_fn_0205bd60();
extern u32 native_fn_ov000_021e9690();
extern u8 native_data_020f6054[];
u32 native_main_0203ee7c(void) {
    u32 temp_r0;
    u8 var_r1;

    if (M2C_FIELD(native_data_020f6054, u8 *, 0xF) == 0) {
        if (M2C_FIELD((void *) native_fn_0205bd60(), s8 *, 0x11) == 0) {
            var_r1 = 0x14;
        } else {
            var_r1 = 0xA;
        }
        M2C_FIELD(native_data_020f6054, u8 *, 0xF) = var_r1;
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0xF) == 0xA) && (native_fn_ov000_021e9690() != 0)) {
        native_fn_020273f0();
        M2C_FIELD(native_data_020f6054, u8 *, 0xF) = 0x14U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0xF) == 0xF) {
        temp_r0 = native_fn_020273f0();
        if ((temp_r0 != 0) && (temp_r0 != 0xC)) {

        } else {
            M2C_FIELD(native_data_020f6054, u8 *, 0xF) = 0x14U;
        }
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0xF) == 0x14) {
        M2C_FIELD(native_data_020f6054, s8 *, 8) = 0xA;
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x1D;
        M2C_FIELD(native_data_020f6054, u8 *, 0xF) = 0U;
    }
    return 0U;
}
