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
extern u32 native_fn_020944f0();
extern u32 native_fn_0209ab84();
extern u32 native_fn_0209ad08();
extern u8 native_data_021d19bc[];
u32 native_main_0209abec(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4) {
    u32 var_r0;

    native_fn_0209ab84();
    if (M2C_FIELD(native_data_021d19bc, void **, 4) != NULL) {
        M2C_FIELD(M2C_FIELD(native_data_021d19bc, void **, 4), s8 *, 0xC) = 1;
    }
    var_r0 = native_fn_0209ad08();
    if (var_r0 == 2) {
        var_r0 = native_fn_020944f0(arg0, arg1, arg2, arg3, arg4);
    }
    return var_r0;
}
