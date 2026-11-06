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
extern u32 native_fn_0201d444();
extern u32 native_fn_02041188();
extern u32 native_fn_ov000_021dfd18();
extern u32 native_fn_ov000_0221276c();
extern u8 native_data_ov000_0222f884[];
u32 native_ov000_0221299c(s32 arg0, s32 arg1) {
    u8 sp0[32];
    u32 var_r4;

    var_r4 = 0;
    if (arg1 > 0) {
        native_fn_0201d444(&sp0, native_data_ov000_0222f884, native_fn_ov000_021dfd18(arg1));
        if (native_fn_02041188(arg0 + 4, native_fn_ov000_0221276c(), &sp0) != 0) {
            var_r4 = 1;
        }
    }
    return var_r4;
}
