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
extern u32 native_fn_020042e0();
extern u8 native_data_020f60e8[];
u32 native_main_02041774(s32 arg0) {
    if (arg0 == 0) {
        native_fn_020042e0(0x04000050, M2C_FIELD(native_data_020f60e8, s32 *, 0x20), M2C_FIELD(native_data_020f60e8, s8 *, 0x1B));
        native_fn_020042e0(0x04001050, M2C_FIELD(native_data_020f60e8, s32 *, 0xC), M2C_FIELD(native_data_020f60e8, s8 *, 7));
        M2C_FIELD(native_data_020f60e8, s32 *, 0) = 0;
        return (u32) native_data_020f60e8;
    }
    native_fn_020042e0(0x04000050, M2C_FIELD(native_data_020f60e8, s32 *, 0xC), M2C_FIELD(native_data_020f60e8, s8 *, 7));
    native_fn_020042e0(0x04001050, M2C_FIELD(native_data_020f60e8, s32 *, 0x20), M2C_FIELD(native_data_020f60e8, s8 *, 0x1B));
    M2C_FIELD(native_data_020f60e8, s32 *, 0) = 1;
    return (u32) native_data_020f60e8;
}
