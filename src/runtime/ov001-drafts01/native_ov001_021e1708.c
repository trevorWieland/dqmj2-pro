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
extern u32 native_fn_0203d294();
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021d908c();
extern u32 native_fn_ov001_021f0ca0();
extern u32 native_fn_ov001_02209490();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_021e1708(u32 arg0, u32 arg1, s32 arg2, void *arg3, s32 arg4, s32 arg5, s32 arg6) {
    u32 temp_r5;
    u32 temp_r5_2;
    u32 var_r1;
    u32 var_r5;

    temp_r5 = native_fn_ov001_02209490(arg3 + 0x22C);
    var_r1 = native_fn_ov001_021f0ca0(arg2, arg3, arg0, 0, arg4);
    if ((arg5 == 0) && (arg6 == 0)) {

    } else if ((s32) var_r1 <= 4) {
        var_r1 = 0;
    }
    temp_r5_2 = native_fn_ov001_021d908c(arg1, var_r1, temp_r5);
    if (arg2 != 0) {
        if (native_fn_ov001_02210ad0(arg2, 0x64, temp_r5_2) != 0) {
            var_r5 = 1;
        } else {
            var_r5 = 0;
        }
    } else if ((s32) native_fn_0203d294(0x64) < (s32) temp_r5_2) {
        var_r5 = 1;
    } else {
        var_r5 = 0;
    }
    if ((arg5 != 0) && ((s32) native_fn_0207b674(0x3B, M2C_FIELD(arg3, s32 *, 0x1E8) + 0x46) > 0)) {
        var_r5 = 0;
    }
    return var_r5;
}
