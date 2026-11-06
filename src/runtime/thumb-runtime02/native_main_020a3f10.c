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
extern u32 native_fn_0209a9e4();
extern u32 native_fn_0209bc5c();
extern u32 native_fn_0209be20();
extern u32 native_fn_020a3dd8();
extern u32 native_fn_020a4144();
extern u32 native_fn_020a4388();
extern u32 native_fn_020a4624();
u32 native_main_020a3f10(u32 arg0, s32 arg1) {
    u32 temp_r4;

    if ((native_fn_0209a9e4() != 0) || ((arg1 == 1) && (native_fn_0209bc5c(arg0) == 0)) || (native_fn_0209be20(arg0) == 0)) {
        return 0U;
    }
    if (native_fn_020a4388(arg0) == 1) {
        return 0U;
    }
    temp_r4 = native_fn_020a4624(arg0);
    if ((s32) temp_r4 < (s32) native_fn_020a4144(arg1)) {
        return 0U;
    }
    if (native_fn_020a3dd8() != 0) {
        return 1U;
    }
    return 0U;
}
