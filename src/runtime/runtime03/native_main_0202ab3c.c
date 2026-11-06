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
extern u32 native_fn_02003888();
extern u32 native_fn_02003db8();
extern u32 native_fn_02007074();
extern u32 native_fn_02008c58();
extern u8 native_data_020edf20[];
extern u8 native_data_020edf24[];
extern u8 native_data_020edf2c[];
u32 native_main_0202ab3c(void) {
    native_fn_02003888(0x1FF);
    native_fn_02008c58(0, (u8 *)0x06800000, 0xA4000);
    native_fn_02003db8();
    native_fn_02008c58(0xC0, (u8 *)0x07000000, 0x400);
    native_fn_02008c58(0xC0, (u8 *)0x07000400, 0x400);
    native_fn_02008c58(0, (u8 *)0x05000000, 0x400);
    native_fn_02008c58(0, (u8 *)0x05000400, 0x400);
    *native_data_020edf20 = 0;
    native_fn_02008c58(0, native_data_020edf24, 8);
    return native_fn_02007074(native_data_020edf2c);
}
