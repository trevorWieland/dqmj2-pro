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
extern u32 native_fn_02089868();
extern u32 native_fn_ov001_021fd84c();
extern u32 native_fn_ov001_022030b8();
extern u32 native_fn_ov001_02203320();
extern u32 native_fn_ov001_022033a4();
extern u32 native_fn_ov001_02203558();
extern u32 native_fn_ov001_02203ccc();
u32 native_ov001_02203dec(void) {
    if ((native_fn_02089868() == 0) && (native_fn_ov001_022030b8() == 0)) {
        return 0U;
    }
    native_fn_ov001_022033a4(1);
    native_fn_02045680(0);
    native_fn_ov001_021fd84c();
    if (native_fn_ov001_02203320(1) != 2) {
        native_fn_ov001_02203ccc(1);
    }
    native_fn_ov001_02203558(1);
    return 0U;
}
