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
extern u32 native_fn_0200616c();
extern u32 native_fn_020ac864();
extern u32 native_fn_020b0600();
extern u32 native_fn_020b0638();
extern u8 native_data_020e1504[];
extern u8 native_data_020e1508[];
u32 native_main_020b2860(u32 arg0, u32 arg1, u32 arg2, u32 arg3, u8 *arg4) {
    u32 var_r0;
    u8 sp0[32];

    if (arg4 == NULL) {
        arg4 = native_data_020e1504;
    }
    var_r0 = native_fn_020b0600(arg0, arg2, 0xC9, arg1);
    if (var_r0 == 0) {
        native_fn_0200616c(&sp0, native_data_020e1508, 1, arg3);
        var_r0 = native_fn_020ac864(arg0, arg2, &sp0);
        if (var_r0 == 0) {
            var_r0 = native_fn_020b0638(arg0, arg2, arg4, -1);
            if (var_r0 == 0) {
                var_r0 = 0;
            }
        }
    }
    return var_r0;
}
