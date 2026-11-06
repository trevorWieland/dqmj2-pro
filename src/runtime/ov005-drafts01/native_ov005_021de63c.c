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
extern u32 native_fn_ov005_021dddec();
typedef struct {
    u8 unknown_0[0x68];
    s32 field_68;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
u32 native_ov005_021de63c(void) {
    native_fn_ov005_021dddec(2, 0x13, 3, 0);
    native_fn_ov005_021dddec(4, 0x13, 3, 3);
    native_fn_ov005_021dddec(5, 0x13, 3, 2);
    native_fn_ov005_021dddec(7, 0x13, 3, 3);
    native_fn_ov005_021dddec(8, 0x13, 3, 7);
    native_fn_ov005_021dddec(0xA, 0x13, 3, 8);
    native_fn_ov005_021dddec(0xC, 0x13, 3, 9);
    if (native_data_ov005_021e9818.field_68 == 1) {
        return native_fn_ov005_021dddec(0xD, 0x13, 3, 1);
    }
    return native_fn_ov005_021dddec(0xD, 0x13, 0, 5);
}
