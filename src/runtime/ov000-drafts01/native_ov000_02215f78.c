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
extern u32 native_fn_020406c8();
extern u32 native_fn_0204617c();
extern u32 native_fn_02049940();
extern u32 native_fn_02078968();
extern u32 native_fn_ov000_02215810();
extern u32 native_fn_ov000_02215814();
extern u32 native_fn_ov000_022184cc();
u32 native_ov000_02215f78(void) {
    if (native_fn_02078968() == 1) {
        native_fn_ov000_022184cc();
    }
    native_fn_ov000_02215810();
    native_fn_ov000_02215814();
    native_fn_0204617c(1, 2);
    native_fn_0204617c(2, 2);
    native_fn_02049940(1);
    return native_fn_020406c8(0);
}
