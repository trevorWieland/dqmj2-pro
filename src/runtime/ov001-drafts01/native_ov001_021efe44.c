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
extern u32 native_fn_020449d4();
extern u32 native_fn_0207afec();
extern u32 native_fn_0207d3d4();
extern u32 native_fn_ov001_02210ba8();
u32 native_ov001_021efe44(u32 arg0, s32 arg1, void *arg2, void *arg3, s32 arg4, s32 arg5) {
    u32 temp_r8;
    u32 var_r7;
    u8 temp_r4;

    var_r7 = arg0;
    if ((((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x1C) >> 0x1C) == 1) && (arg5 == 0)) {
        temp_r4 = M2C_FIELD(arg2, u8 *, 0x1FD);
        if ((s32) temp_r4 > 0) {
            temp_r8 = native_fn_020449d4(M2C_FIELD(M2C_FIELD(arg3, void **, 0x1E8), s16 *, 0x2A));
            var_r7 = native_fn_0207d3d4(temp_r4, var_r7, (u8) ((u32) (M2C_FIELD(temp_r8, u16 *, 4) << 0x18) >> 0x1C), native_fn_ov001_02210ba8(arg3), arg4, arg1);
        }
    }
    return var_r7;
}
