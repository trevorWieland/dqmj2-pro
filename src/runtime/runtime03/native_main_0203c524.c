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
extern u32 native_fn_02008c58();
extern u8 native_data_020f5bf0[];
extern u8 native_data_020f5bf4[];
extern u8 native_data_020f5c00[];
extern u8 native_data_020f5c18[];
u32 native_main_0203c524(void) {
    native_fn_02008c58(0, native_data_020f5c00, 0x18);
    native_fn_02008c58(0, native_data_020f5bf4, 0xC);
    native_fn_02008c58(0, native_data_020f5c18, 0x300);
    *native_data_020f5bf0 = 0;
    return (u32) native_data_020f5bf0;
}
