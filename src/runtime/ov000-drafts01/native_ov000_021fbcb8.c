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
extern u32 native_fn_ov000_021fb7e8();
extern u32 native_fn_ov000_021fb8a8();
extern u32 native_fn_ov000_021fb8f8();
extern u32 native_fn_ov000_021fbad8();
extern u8 native_data_ov000_0222f42c[];
extern u8 native_data_ov000_02237170[];
u32 native_ov000_021fbcb8(void) {
    native_fn_ov000_021fbad8(native_data_ov000_02237170, 0);
    if ((native_fn_ov000_021fb8a8() == 0xFF) && (native_fn_ov000_021fb7e8(native_data_ov000_02237170) == 0xFF)) {
        *native_data_ov000_0222f42c = 4;
    } else if ((native_fn_ov000_021fb8a8() != 0xFF) && ((native_fn_ov000_021fb8f8(0x36, native_data_ov000_02237170) != 0xFF) || (native_fn_ov000_021fb8f8(0x37, native_data_ov000_02237170) != 0xFF))) {
        *native_data_ov000_0222f42c = 2;
    } else if ((native_fn_ov000_021fb7e8(native_data_ov000_02237170) != 0xFF) && ((native_fn_ov000_021fb8f8(0x2F, native_data_ov000_02237170) != 0xFF) || (native_fn_ov000_021fb8f8(0x30, native_data_ov000_02237170) != 0xFF) || (native_fn_ov000_021fb8f8(0x31, native_data_ov000_02237170) != 0xFF) || (native_fn_ov000_021fb8f8(0x32, native_data_ov000_02237170) != 0xFF) || (native_fn_ov000_021fb8f8(0x33, native_data_ov000_02237170) != 0xFF))) {
        *native_data_ov000_0222f42c = 2;
    } else {
        *native_data_ov000_0222f42c = 3;
    }
    return (u32) *native_data_ov000_0222f42c;
}
