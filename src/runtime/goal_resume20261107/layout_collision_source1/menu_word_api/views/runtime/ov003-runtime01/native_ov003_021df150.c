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
#define NULL ((void *)0)
extern u32 native_fn_02048f7c();
#include "../../../api.h"
extern u32 native_fn_020c48bc();
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
extern u32 native_fn_ov003_021dfd18();
u32 native_ov003_021df150(u32 arg0, u32 arg1) {
    native_fn_020c48bc();
    native_fn_020c48d0(0x14, 1, arg0);
    native_fn_020c48e8(arg1);
    native_fn_020c484c(native_fn_02048f7c(1));
    return native_fn_ov003_021dfd18(0);
}
