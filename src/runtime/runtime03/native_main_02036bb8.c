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
extern u32 native_fn_02008be0();
extern u8 native_data_020f0f08[];
extern u8 native_data_020f1008[];
extern u8 native_data_020f1408[];
extern u8 native_data_020f1448[];
extern u8 native_data_020f1548[];
extern u8 native_data_020f1948[];
extern u8 native_data_020f1988[];
extern u8 native_data_020f1a88[];
extern u8 native_data_020f1e88[];
u32 native_main_02036bb8(void) {
    native_fn_02008be0(0xC0, native_data_020f1008, 0x400);
    native_fn_02008be0(0xC0, native_data_020f1548, 0x400);
    native_fn_02008be0(0xC0, native_data_020f1a88, 0x400);
    native_fn_02008be0(0xFFFF, native_data_020f0f08, 0x100);
    native_fn_02008be0(0xFFFF, native_data_020f1448, 0x100);
    native_fn_02008be0(0xFFFF, native_data_020f1988, 0x100);
    native_fn_02008be0(0xFFFF, native_data_020f1408, 0x40);
    native_fn_02008be0(0xFFFF, native_data_020f1948, 0x40);
    return native_fn_02008be0(0xFFFF, native_data_020f1e88, 0x40);
}
