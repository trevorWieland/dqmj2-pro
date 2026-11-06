#define NULL ((void *)0)
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
extern u32 native_fn_02008430();
extern u32 native_fn_020197e4();
extern u8 native_data_020ec3c0[];
u32 native_main_02019788(u32 arg0, s32 arg1) {
    s32 var_r0;

    if ((arg1 & 0x3F) == 0x11) {
        if (M2C_FIELD(native_data_020ec3c0, s32 *, 0xC) != 0) {
            return (u32) native_data_020ec3c0;
        }
        var_r0 = 0;
        if (M2C_FIELD(native_data_020ec3c0, s32 (**)(), 0x18) != NULL) {
            var_r0 = M2C_FIELD(native_data_020ec3c0, s32 (**)(), 0x18)();
        }
        if (var_r0 != 0) {
            native_fn_020197e4();
        }
        M2C_FIELD(native_data_020ec3c0, s32 *, 0xC) = 1;
        return (u32) native_data_020ec3c0;
    }
    return native_fn_02008430();
}
