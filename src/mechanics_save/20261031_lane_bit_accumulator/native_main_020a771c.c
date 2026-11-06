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
u32 native_main_020a771c(u32 arg0) {
    u32 var_r1;

    var_r1 = 5;
    if (2 & arg0) {
        var_r1 += 4;
    }
    if (8 & arg0) {
        var_r1 += 4;
    }
    if (0x10 & arg0) {
        var_r1 += 2;
    }
    if (arg0 & 0x20) {
        var_r1 += 2;
    }
    return var_r1;
}
