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
extern u32 native_fn_020273d8();
extern u32 native_fn_020404f0();
extern u32 native_fn_02067380();
extern u32 native_fn_020675e8();
extern u32 native_fn_ov000_021e4e9c();
extern u8 native_data_020f6054[];
u32 native_main_0203e55c(void) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_fn_02067380();
    temp_r0 = native_fn_020675e8();
    if ((temp_r4 != 0) && (temp_r0 != 0)) {
        if (M2C_FIELD(native_data_020f6054, s32 *, 0x44) == 0) {
            native_fn_020273d8(1);
            M2C_FIELD(native_data_020f6054, s32 *, 0x44) = 0xA;
        } else if (M2C_FIELD(native_data_020f6054, s32 *, 0x44) == 0xA) {
            if (native_fn_ov000_021e4e9c(0x89) != 0) {
                native_fn_020404f0(0x31);
            } else {
                native_fn_020404f0(5);
            }
            M2C_FIELD(native_data_020f6054, s32 *, 0x44) = 0;
        }
    }
    return 0U;
}
