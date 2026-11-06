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
extern u32 native_fn_02029c88();
extern u32 native_fn_02029cc4();
extern u32 native_fn_02029cf8();
extern u32 native_fn_02029d2c();
extern u32 native_fn_02029d5c();
u32 native_ov000_021d9960(void *arg0) {
    if (M2C_FIELD(arg0, u8 *, 8) != 0) {
        native_fn_02029c88(M2C_FIELD(arg0, u8 *, 0), M2C_FIELD(arg0, u8 *, 1), M2C_FIELD(arg0, u8 *, 2));
        native_fn_02029cc4(M2C_FIELD(arg0, u8 *, 3));
        native_fn_02029cf8(M2C_FIELD(arg0, u8 *, 4));
        native_fn_02029d2c(M2C_FIELD(arg0, u8 *, 5));
        native_fn_02029d5c(M2C_FIELD(arg0, u16 *, 6));
    }
    return 0U;
}
