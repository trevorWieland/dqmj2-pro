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
extern u32 native_fn_ov006_021e6488();
extern u32 native_fn_ov006_021e808c();
extern u32 native_fn_ov006_021e81e8();
extern u32 native_fn_ov006_021eb9a4();
extern u8 native_data_ov006_0220bb6c[];
extern u8 native_data_ov006_0220bb74[];
u32 native_ov006_02204a84(void) {
    native_fn_ov006_021e6488();
    native_fn_ov006_021e81e8(1, native_data_ov006_0220bb6c, 7, native_data_ov006_0220bb74, 0x17, 0, 0, 0, 0);
    native_fn_ov006_021eb9a4(0xA, 1, 1);
    return native_fn_ov006_021e808c();
}
