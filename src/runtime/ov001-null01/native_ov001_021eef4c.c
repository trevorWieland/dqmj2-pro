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
extern u32 native_fn_0205d5bc();
extern u32 native_fn_0205d750();
u32 native_ov001_021eef4c(void) {
    u8 *var_r0;
    void *temp_r1;
    s32 var_r2;

    var_r0 = native_fn_0205d750(0);
    var_r2 = 0;
    do {
        if ((M2C_FIELD(var_r0, u8 *, 0) == 3) && (M2C_FIELD(var_r0, u8 *, 2) == 1)) {
            temp_r1 = M2C_FIELD(var_r0, void **, 0x118);
            if (temp_r1 != NULL) {
                M2C_FIELD(var_r0, u8 *, 6) = (u8) M2C_FIELD(temp_r1, u8 *, 0x31D);
            }
        }
        var_r2 += 1;
        var_r0 += 0x11C;
    } while (var_r2 < 0x20);
    return native_fn_0205d5bc();
}
