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
extern u32 native_fn_ov006_021d77f8();
extern u32 native_fn_ov006_021d7860();
extern u32 native_fn_ov006_021d79e4();
extern u32 native_fn_ov006_021d7d28();
extern u32 native_fn_ov006_021db410();
extern u8 native_data_ov006_0220cc80[];
u32 native_ov006_021db3c0(void) {
    native_fn_ov006_021d7860();
    native_fn_ov006_021d77f8(7);
    native_fn_ov006_021d7d28(native_data_ov006_0220cc80, 0x20);
    native_fn_ov006_021d79e4(0, 0xF, 2, 0x81);
    native_fn_ov006_021d79e4(1, 0xF, 2, 0x82);
    return native_fn_ov006_021db410();
}
