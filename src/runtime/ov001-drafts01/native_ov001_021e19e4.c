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
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021d90c4();
extern u32 native_fn_ov001_021f08ec();
extern u32 native_fn_ov001_021f0d10();
u32 native_ov001_021e19e4(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r4;

    temp_r4 = native_fn_ov001_021f08ec(arg2, arg0);
    if ((native_fn_ov001_021f0d10(arg1, arg2, arg0, 1) == 6) && ((native_fn_ov001_021d90c4(temp_r4, 0) != 1) || (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x1C) >> 0x1C) != 1))) {
        return 1U;
    }
    return 0U;
}
