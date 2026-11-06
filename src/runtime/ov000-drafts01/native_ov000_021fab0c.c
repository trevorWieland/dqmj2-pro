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
extern u32 native_fn_02045680();
extern u32 native_fn_ov000_021f7fcc();
extern u32 native_fn_ov000_021f8398();
extern u32 native_fn_ov000_021f895c();
extern u32 native_fn_ov000_02215698();
extern u32 native_fn_ov000_02215850();
extern u32 native_fn_ov000_02215a7c();
extern u32 native_fn_ov000_022162b4();
extern u32 native_fn_ov000_02217440();
u32 native_ov000_021fab0c(void) {
    native_fn_ov000_02215698();
    native_fn_ov000_022162b4(M2C_FIELD((void *) native_fn_ov000_02217440(), s8 *, 0x10), 0x7F);
    native_fn_ov000_021f895c();
    native_fn_ov000_021f8398();
    native_fn_ov000_02215850();
    if (native_fn_ov000_02215a7c() != 0) {
        native_fn_ov000_021f7fcc();
    }
    native_fn_02045680(2);
    native_fn_02045680(3);
    return 0U;
}
