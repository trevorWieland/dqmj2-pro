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
extern u32 native_fn_0201d69c();
extern u32 native_fn_020a8e7c();
extern u32 native_fn_020ac7c0();
extern u32 native_fn_020ac7c4();
extern u32 native_fn_020ac864();
extern u8 native_data_020e10c0[];
extern u8 native_data_020e10c4[];
u32 native_main_020b0638(u32 arg0, void *arg1, u8 *arg2, u32 arg3) {
    u32 var_r0;
    u8 *var_r4;
    u32 var_r6;
    u8 sp0[32];

    var_r4 = arg2;
    var_r6 = arg3;
    if (arg1 == NULL) {
        return 3U;
    }
    if (var_r4 == NULL) {
        var_r4 = native_data_020e10c0;
    }
    if (var_r6 == -1U) {
        var_r6 = native_fn_0201d69c(var_r4);
    }
    native_fn_0200616c(&sp0, native_data_020e10c4, var_r6);
    var_r0 = native_fn_020ac864(arg0, arg1, &sp0);
    if (var_r0 == 0) {
        var_r0 = native_fn_020ac7c4(arg0, arg1, var_r4, var_r6);
        if (var_r0 == 0) {
            var_r0 = native_fn_020ac7c0(arg0, arg1, 0);
            if (var_r0 == 0) {
                M2C_FIELD(arg1, s32 *, 0x14) = (s32) (native_fn_020a8e7c(0) + 0x2710);
                var_r0 = 0;
            }
        }
    }
    return var_r0;
}
