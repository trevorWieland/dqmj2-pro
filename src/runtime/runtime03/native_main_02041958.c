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
extern u32 native_fn_02008d78();
extern u8 native_data_020f6114[];
extern u8 native_data_020f621c[];
extern u8 native_data_020f65b4[];
u32 native_main_02041958(void) {
    native_fn_02008d78(native_data_020f621c, 0, 0x398);
    native_fn_02008d78(native_data_020f65b4, 0, 0x400);
    return native_fn_02008d78(native_data_020f6114, 0, 0x108);
}
