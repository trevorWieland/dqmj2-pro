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
extern u32 native_fn_02026144();
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b94c();
extern u32 native_fn_ov001_021dbd3c();
extern u32 native_fn_ov001_021dbd8c();
u32 native_ov001_021ef4cc(u32 arg0, u32 arg1, void *arg2, u32 arg3, s32 arg4, s32 arg5) {
    s32 temp_r0;
    s32 temp_r5;
    u32 temp_r0_2;
    u32 temp_r4;
    u32 temp_r4_2;
    u32 temp_r4_3;
    u32 var_r9;

    var_r9 = arg0;
    if ((((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x1C) >> 0x1C) == 1) || (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x14) >> 0x1C) == 7)) {
        temp_r4 = native_fn_ov001_021dbd3c(arg2);
        temp_r0 = (s32) native_fn_ov001_021dbd8c(arg3);
        temp_r5 = (s32) (temp_r4 - (temp_r0 >> 1)) >> 1;
        if (temp_r5 <= 0) {
            var_r9 += (M2C_FIELD(arg2, u8 *, 0x356) + native_fn_0207b94c(2, arg4)) - 1;
        } else if ((temp_r5 <= (s32) ((s32) temp_r4 >> 4)) || ((s32) (temp_r0 >> 1) >= (s32) temp_r4)) {
            var_r9 += (M2C_FIELD(arg2, u8 *, 0x356) + native_fn_0207b94c(((s32) temp_r4 >> 4) + 1, arg4)) - 1;
        } else {
            temp_r4_2 = native_fn_0207b94c(temp_r5 >> 3, arg4);
            var_r9 += M2C_FIELD(arg2, u8 *, 0x356) + (temp_r5 + (temp_r4_2 - (temp_r5 >> 4)) + (native_fn_0207b94c(3, arg4) - 2));
        }
        if (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x14) >> 0x1C) == 7) {
            temp_r4_3 = native_fn_0207afec(arg1);
            var_r9 = native_fn_02026144(var_r9 * M2C_FIELD(temp_r4_3, s16 *, 0x10), M2C_FIELD((void *) native_fn_0207afec(arg1), s16 *, 0x12));
        }
        if (arg5 != 0) {
            temp_r0_2 = var_r9 * 3;
            var_r9 = (u32) ((s32) (temp_r0_2 + (temp_r0_2 >> 0x1F)) >> 1);
        }
        if ((s32) var_r9 < 0) {
            var_r9 = 0;
        }
    }
    return var_r9;
}
