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
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
extern u32 native_fn_020b6cb4();
extern u8 native_data_021d2bc4[];
u32 native_main_020b6e6c(void) {
    u32 var_r0;
    s32 var_r5;

    if ((*(u32 *)native_data_021d2bc4 == 0) || (native_fn_020a8640() == 0)) {
        return native_fn_020b6cb4(0);
    }
    var_r0 = native_fn_020a8640(*(u32 *)native_data_021d2bc4);
    var_r5 = var_r0 - 1;
    if (var_r5 >= 0) {
        do {
            native_fn_020a8644(*(u32 *)native_data_021d2bc4, var_r5);
            var_r0 = native_fn_020b6cb4();
            var_r5 -= 1;
        } while (var_r5 >= 0);
    }
    return var_r0;
}
