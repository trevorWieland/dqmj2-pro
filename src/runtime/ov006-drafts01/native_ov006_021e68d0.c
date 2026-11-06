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
extern u32 native_fn_0203cb2c();
extern u32 native_fn_0203cb64();
extern u32 native_fn_020455c8();
extern u32 native_fn_0205dbf0();
extern u32 native_fn_0205df8c();
extern u32 native_fn_02084920();
extern u32 native_fn_ov006_021e6b3c();
extern u32 native_fn_ov006_021e72b4();
extern u32 native_fn_ov006_021e9e78();
extern u32 native_fn_ov006_021eba54();
extern u8 native_data_020daef8[];
extern u8 native_data_020daf0c[];
extern u8 native_data_020dc348[];
extern u8 native_data_020dc368[];
extern u8 native_data_ov006_02218da8[];
extern u8 native_data_ov006_02218de4[];
u32 native_ov006_021e68d0(void) {
    native_fn_ov006_021e9e78();
    native_fn_ov006_021eba54();
    native_fn_ov006_021e72b4();
    native_fn_ov006_021e6b3c();
    native_fn_020455c8(1);
    native_fn_0205dbf0(1, native_data_ov006_02218de4, native_data_020daf0c, native_data_020daef8, 9);
    native_fn_0205dbf0(1, native_data_ov006_02218da8, native_data_020dc368, native_data_020dc348, 0x10);
    native_fn_0205df8c(0);
    native_fn_02084920();
    native_fn_0203cb2c();
    return native_fn_0203cb64();
}
