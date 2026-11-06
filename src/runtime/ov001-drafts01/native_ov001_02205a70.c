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
extern u32 native_fn_ov001_02204924();
u32 native_ov001_02205a70(void *arg0) {
    s8 var_r4;
    s8 var_r5;
    s8 var_r6;

    var_r5 = -1;
    var_r4 = 0;
loop_1:
    var_r6 = M2C_FIELD(arg0, s32 *, 0x2C) + 1 + var_r4;
    if ((s32) var_r6 >= 0x13) {
        var_r6 -= 0x13;
    }
    if (native_fn_ov001_02204924((s8) M2C_FIELD(arg0, s32 *, 0x30), (s8) M2C_FIELD(arg0, s32 *, 0x34), var_r6) != 0) {
        var_r5 = var_r6;
    } else {
        var_r4 += 1;
        if ((s32) var_r4 < 0x13) {
            goto loop_1;
        }
    }
    return (u32) var_r5;
}
