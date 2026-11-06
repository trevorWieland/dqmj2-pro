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
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021db8d0();
u32 native_ov001_0220f354(void *arg0, u32 arg1, u32 arg2) {
    s32 var_r5;
    void *var_r7;

    var_r7 = arg0;
    var_r5 = 0;
loop_1:
    if ((native_fn_ov001_021db8d0(var_r7) != 0) && ((s32) native_fn_0207b674(0xD, M2C_FIELD(var_r7, s32 *, 0x1E8) + 0x46) > 0)) {
        return 1U;
    }
    var_r5 += 1;
    var_r7 += 0x440;
    if (var_r5 >= 3) {
        return arg2;
    }
    goto loop_1;
}
