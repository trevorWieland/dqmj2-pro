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
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dbe68();
extern u32 native_fn_ov001_022187dc();
u32 native_ov001_0221bb5c(void *arg0) {
    s32 var_r4;
    s32 var_r5;

    var_r5 = M2C_FIELD(arg0, s32 *, 8);
    var_r4 = 0;
loop_1:
    if ((native_fn_ov001_021db8d0(var_r5) != 0) && ((s32) native_fn_ov001_021dbe68(var_r5) <= 1)) {
        return 1U;
    }
    var_r4 += 1;
    var_r5 += 0x440;
    if (var_r4 >= 3) {
        return native_fn_ov001_022187dc(M2C_FIELD(arg0, s32 *, 8), 4, -1, 2);
    }
    goto loop_1;
}
