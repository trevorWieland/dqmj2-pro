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
extern u32 native_fn_0203dd48();
extern u32 native_fn_02040434();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e4e9c();
extern u8 native_data_020f6054[];
u32 native_main_0203fe60(void) {
    u32 var_r4;

    if (native_fn_ov000_021e4e9c(0x84) != 0) {
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x31;
        var_r4 = 1;
    } else {
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 5;
        var_r4 = 0;
    }
    native_fn_ov000_021e1894(0);
    native_fn_0203dd48();
    native_fn_02040434();
    return var_r4;
}
