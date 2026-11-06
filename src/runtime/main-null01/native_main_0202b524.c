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
u32 native_main_0202b524(void *arg0) {
    u32 var_r0;
    s32 temp_r1;
    void *var_r2;

    var_r2 = M2C_FIELD(arg0, void **, 0x24);
    var_r0 = 0;
    if (var_r2 == NULL) {
        return 0U;
    }
    do {
        temp_r1 = M2C_FIELD(var_r2, s32 *, 4);
        var_r2 = M2C_FIELD(var_r2, void **, 0xC);
        var_r0 += temp_r1;
    } while (var_r2 != NULL);
    return var_r0;
}
