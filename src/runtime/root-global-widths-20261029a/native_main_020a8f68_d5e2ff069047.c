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
extern u8 native_data_020e0378[];
u32 native_main_020a8f68(s32 arg0) {
    s32 var_r1;

    if (arg0 != 0) {
        var_r1 = 0x7FFFFFFF & arg0;
    } else {
        var_r1 = 1;
    }
    *(u32 *)native_data_020e0378 = var_r1;
    return (u32) native_data_020e0378;
}
