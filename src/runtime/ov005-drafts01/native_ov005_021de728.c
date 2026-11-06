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
extern u32 native_fn_020456ac();
extern u32 native_fn_02048f6c();
extern u32 native_fn_ov005_021dddec();
extern u32 native_fn_ov005_021dde00();
u32 native_ov005_021de728(void) {
    native_fn_ov005_021dde00(3, 0x13, 0, 0xD, 0x18);
    native_fn_ov005_021dddec(1, 0x13, 0, 0xA);
    native_fn_ov005_021dde00(6, 0x13, 0, 0xD, 0x10);
    native_fn_ov005_021dde00(9, 0x13, 0, 0xD, 0x40);
    native_fn_ov005_021dde00(0xB, 0x13, 0, 0xD, 0x18);
    native_fn_ov005_021dddec(0xE, 0x13, 0, 5);
    return native_fn_020456ac(0, native_fn_02048f6c(0), 2, 4, 2, 2);
}
