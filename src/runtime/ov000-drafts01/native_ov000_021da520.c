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
u32 native_ov000_021da520(void *arg0, s8 arg1, s32 arg2, s32 arg3, void *arg4) {
    s32 var_lr;
    void *var_r4;

    M2C_FIELD(arg0, s8 *, 0) = 1;
    M2C_FIELD(arg0, s8 *, 1) = arg1;
    M2C_FIELD(arg0, s32 *, 4) = arg2;
    M2C_FIELD(arg0, s32 *, 0xC) = arg3;
    var_lr = 0;
    M2C_FIELD(arg0, s32 *, 8) = 0;
    if ((s32) arg1 > 0) {
        var_r4 = arg4;
        do {
            var_lr += 1;
            M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) + M2C_FIELD(var_r4, s32 *, 0x10));
            var_r4 += 0xC;
        } while (var_lr < (s32) arg1);
    }
    M2C_FIELD(arg0, s32 *, 8) = (s32) (M2C_FIELD(arg0, s32 *, 8) + arg2);
    return (u32) arg0;
}
