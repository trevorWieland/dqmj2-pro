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
extern u32 native_fn_0204617c();
extern u32 native_fn_02049940();
extern u32 native_fn_0204bb18();
extern u32 native_fn_0204bb28();
extern u32 native_fn_ov006_021e7ff0();
u32 native_ov006_021e71b0(void) {
    if (native_fn_0204bb18() == 0) {
        native_fn_ov006_021e7ff0();
        native_fn_0204bb28(0);
    }
    native_fn_0204617c(0, 1);
    return native_fn_02049940(0);
}
