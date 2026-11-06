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
extern u32 native_fn_01ff8604();
extern u32 native_fn_020642dc();
extern u32 native_fn_02064488();
extern u32 native_fn_020ba564();
extern u32 native_fn_ov006_021ded5c();
extern u32 native_fn_ov006_021def28();
extern u32 native_fn_ov006_021e2c8c();
extern u32 native_fn_ov006_021e2ef4();
u32 native_ov006_021e2c9c(void) {
    if (native_fn_020642dc() == 0x25) {
        return native_fn_ov006_021e2c8c(0);
    }
    if (native_fn_020ba564() == 0) {
        native_fn_ov006_021ded5c(0xF, 3, 3);
        native_fn_ov006_021def28(1);
        native_fn_01ff8604(0);
        native_fn_02064488(2);
        return native_fn_ov006_021e2c8c(3);
    }
    native_fn_ov006_021ded5c(0xF, 0xA, 0xB);
    native_fn_ov006_021def28(1);
    native_fn_ov006_021e2c8c(1);
    return native_fn_ov006_021e2ef4();
}
