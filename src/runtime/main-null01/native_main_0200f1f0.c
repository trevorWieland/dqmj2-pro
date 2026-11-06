#define NULL ((void *)0)
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
u32 native_main_0200f1f0(void *arg0) {
    u32 temp_r0;
    void *var_r4;

    var_r4 = arg0;
    if (var_r4 == NULL) {
        return (u32) arg0;
    }
    do {
        temp_r0 = M2C_FIELD(var_r4, u32 (**)(s32), 0)(M2C_FIELD(var_r4, s32 *, 4));
        var_r4 = M2C_FIELD(var_r4, void **, 8);
    } while (var_r4 != NULL);
    return temp_r0;
}
