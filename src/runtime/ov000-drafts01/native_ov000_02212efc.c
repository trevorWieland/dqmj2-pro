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
u32 native_ov000_02212efc(void *arg0, s32 arg1) {
    u32 var_r3;

    var_r3 = 0;
    if ((M2C_FIELD(arg0, u8 *, 0xDC) != 0) && ((s32) M2C_FIELD(arg0, s32 *, 0) > 0) && (arg1 < 4) && (M2C_FIELD((arg0 + (arg1 * 8)), s32 *, 0xC0) != 0)) {
        var_r3 = 1;
    }
    return var_r3;
}
