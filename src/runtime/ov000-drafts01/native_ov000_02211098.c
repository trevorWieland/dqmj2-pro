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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02008c14();
extern u8 native_data_ov000_02240af4[];
extern u8 native_data_ov000_02240b54[];
extern u8 native_data_ov000_02240bb4[];
extern u8 native_data_ov000_02240fbc[];
extern u8 native_data_ov000_0224157c[];
u32 native_ov000_02211098(void) {
    native_fn_02008c14(0, native_data_ov000_02240fbc, 0x5C0);
    native_fn_02008c14(0, native_data_ov000_02240bb4, 0xC0);
    native_fn_02008c14(0, native_data_ov000_02240af4, 0x60);
    native_fn_02008c14(0, native_data_ov000_02240b54, 0x60);
    return native_fn_02008c14(0, native_data_ov000_0224157c, 0x21C0);
}
