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
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021e1a60();
extern u32 native_fn_ov001_022189cc();
u32 native_ov001_02218a54(u32 arg0, s32 arg1, u32 arg2, s32 arg3, s32 arg4) {
    s32 sp24;
    s32 sp20;
    s32 sp1C;
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;
    s32 var_r9;
    u32 temp_r0;

    var_r5 = 0;
    var_r9 = arg1;
    var_r6 = 0;
    var_r4 = 0;
    do {
        if (native_fn_ov001_021db8d0(var_r9) != 0) {
            sp24 = 0;
            sp20 = 0;
            sp1C = 1;
            if (arg3 != 0) {
                native_fn_ov001_021e1a60(arg2, arg0, var_r9, 0, 0, 0, &sp24, 0, &sp20, &sp1C, 0);
            }
            temp_r0 = native_fn_ov001_022189cc(arg0, var_r9, arg2, arg4);
            if ((sp1C != 0) || ((s32) temp_r0 >= 5)) {
                var_r6 += temp_r0;
                var_r5 += 1;
            }
        }
        var_r4 += 1;
        var_r9 += 0x440;
    } while (var_r4 < 3);
    if (var_r5 > 0) {
        var_r6 = (s32) native_fn_02026144(var_r6, var_r5);
    }
    return (u32) var_r6;
}
