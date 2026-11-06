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
extern u32 native_fn_ov001_021e6764();
extern u32 native_fn_ov001_022180e0();
u32 native_ov001_021e6e40(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    if (((M2C_FIELD((void *) native_fn_ov001_022180e0(arg3), u8 *, 4) & 1) || (M2C_FIELD((void *) native_fn_ov001_022180e0(arg3), u8 *, 4) & 8)) && ((s32) native_fn_ov001_021e6764(arg0, arg1, arg2, arg3, 0x2710, 0) < 0)) {
        return 1U;
    }
    return 0U;
}
