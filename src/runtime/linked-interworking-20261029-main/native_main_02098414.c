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
extern u32 native_fn_02006b7c();
extern u32 native_fn_0200708c();
extern u32 native_fn_02007110();
extern u32 native_fn_02008360();
extern u32 native_fn_02092338();
u32 native_main_02098414(void *arg0) {
    if (M2C_FIELD(arg0, s32 *, 0x1130) == 1) {
        native_fn_02008360(arg0 + 0x19D4);
        native_fn_02092338(arg0 + 0x19D4, 0x20);
    }
    native_fn_0200708c(arg0 + 0x1BF8);
    if (M2C_FIELD(arg0, s32 *, 0x1C10) == 1) {
        native_fn_02007110(arg0 + 0x1BF8);
        return 0U;
    }
    native_fn_02007110(arg0 + 0x1BF8);
    native_fn_02006b7c(0xA);
    return 1U;
}
