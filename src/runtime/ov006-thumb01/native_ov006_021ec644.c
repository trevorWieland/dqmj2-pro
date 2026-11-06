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
u32 native_ov006_021ec644(s32 arg0, s32 arg1) {
    u32 var_r0;
    s32 temp_r1;
    s32 temp_r2;

    temp_r2 = arg0 & arg1;
    temp_r1 = ~arg1;
    var_r0 = ((arg0 & temp_r1) + 1) | temp_r2;
    if (var_r0 >= (u32) (temp_r1 | temp_r2)) {
        var_r0 = 1 | temp_r2;
    }
    return var_r0;
}
