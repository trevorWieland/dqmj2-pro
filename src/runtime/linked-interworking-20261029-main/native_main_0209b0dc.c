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
extern u32 native_fn_0201d69c();
extern u32 native_fn_02099d6c();
extern u32 native_fn_02099dc8();
extern u32 native_fn_02099df4();
extern u32 native_fn_0209aa38();
extern u32 native_fn_0209aa64();
extern u8 native_data_020e0154[];
u32 native_main_0209b0dc(u8 *arg0, u32 arg1) {
    u32 var_r0;

    if (native_fn_02099d6c(native_fn_0209aa38, native_fn_0209aa64) == 0) {
        return 0U;
    }
    if (native_fn_0201d69c(arg0) == 0) {
        var_r0 = native_fn_02099df4(native_data_020e0154, arg1);
    } else {
        var_r0 = native_fn_02099df4(arg0, arg1);
    }
    if (var_r0 == 0) {
        native_fn_02099dc8();
        return 0U;
    }
    return 1U;
}
