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
extern u32 native_fn_0201b1bc();
u32 native_main_020b3bb8(void *arg0, s32 arg1, s32 arg2) {
    s32 temp_r0_2;
    u32 temp_r0;
    s32 var_r3;

    var_r3 = arg1;
    if (var_r3 == -1) {
        var_r3 = M2C_FIELD(arg0, u32 *, 8) - arg2;
    }
    temp_r0_2 = M2C_FIELD(arg0, s32 *, 0) + var_r3;
    native_fn_0201b1bc(temp_r0_2, temp_r0_2 + arg2, (M2C_FIELD(arg0, u32 *, 8) - var_r3) - arg2);
    temp_r0 = M2C_FIELD(arg0, u32 *, 8) - arg2;
    M2C_FIELD(arg0, u32 *, 8) = temp_r0;
    return temp_r0;
}
