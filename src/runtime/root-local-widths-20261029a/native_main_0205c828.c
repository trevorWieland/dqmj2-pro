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
extern u32 native_fn_0202aa58();
extern u32 native_fn_0202aab4();
extern u32 native_fn_0205c404();
extern u32 native_fn_0205c49c();
u32 native_main_0205c828(u32 arg0, s32 arg1) {
    u8 *temp_r0;
    u32 var_r5;

    var_r5 = 0;
    if ((native_fn_0202aa58(0) != 0) && (native_fn_0202aab4(0) != 0)) {
        temp_r0 = native_fn_0205c404(arg0);
        if (temp_r0 != NULL) {
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 0, arg1);
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 4, arg1);
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 1, arg1);
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 2, arg1);
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 3, arg1);
            native_fn_0205c49c(*(u32 *)temp_r0, temp_r0, arg0, 5, arg1);
            var_r5 = 1;
        }
    }
    return var_r5;
}
