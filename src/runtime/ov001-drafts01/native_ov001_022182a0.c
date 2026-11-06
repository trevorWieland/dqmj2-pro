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
extern u32 native_fn_020443ec();
extern u32 native_fn_020444a8();
extern u8 native_data_ov001_02243dc8[];
u32 native_ov001_022182a0(s32 arg0, s32 arg1, s32 arg2) {
    if ((native_fn_020444a8() != 0) || (arg0 == 0) || (native_fn_020443ec() == 3) || (native_fn_020443ec() == 6)) {
        return (u32) *(arg1 + (native_data_ov001_02243dc8 + (arg2 * 8)));
    }
    return (u32) *(arg1 + 5 + (native_data_ov001_02243dc8 + (arg2 * 8)));
}
