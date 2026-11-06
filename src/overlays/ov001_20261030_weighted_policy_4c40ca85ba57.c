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
#define NULL ((void *)0)
extern u32 native_fn_0203d294();
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021e2b88();
extern u32 native_fn_ov001_021e6db4();
extern u32 native_fn_ov001_021e6e40();
extern u8 native_data_ov001_0222ec5c[];
u32 native_ov001_021e6ec4(void *arg0, u32 arg1, u32 arg2, s32 arg3) {
    s32 var_r0;
    u32 temp_r0;
    u8 temp_r1;
    s32 var_r2;
    s32 var_r3;
    u8 var_r5;
    s32 var_r6;
    s32 var_ip;
    const u8 *weights;

    var_r5 = 0;
    var_r6 = 0;
    if (arg3 >= 4) {
        return 0U;
    }
    weights = native_data_ov001_0222ec5c + arg3 * 6;
loop_3:
    temp_r0 = native_fn_0203d294(0x100);
    var_r2 = 0;
loop_4:
    var_ip = 0;
    var_r3 = 0;
    if (var_r2 >= 0) {
        do {
            temp_r1 = weights[var_r3];
            var_r3 += 1;
            var_ip += temp_r1;
        } while (var_r3 <= var_r2);
    }
    if ((s32) temp_r0 < var_ip) {
        var_r5 = M2C_FIELD((M2C_FIELD(arg0, s32 *, 0x1E8) + var_r2), u8 *, 8);
    } else {
        var_r2 += 1;
        if (var_r2 < 6) {
            goto loop_4;
        }
    }
    if (native_fn_ov001_021e6e40(arg0, arg1, arg2, var_r5) != 0) {
        var_r5 = 0;
    }
    if ((((s32) native_fn_ov001_021e2b88() >= 2) && (M2C_FIELD((void *) native_fn_0207afec(var_r5), s8 *, 0x26) != 0)) || (native_fn_ov001_021e6db4(M2C_FIELD(arg0, u8 *, 0x31E), var_r5, M2C_FIELD(arg0, u8 *, 0x31F)) != 0)) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    var_r6 += 1;
    if ((var_r0 != 0) && (var_r6 <= 0xC)) {
        goto loop_3;
    }
    if (var_r6 > 0xC) {
        var_r5 = 0;
    }
    return (u32) var_r5;
}
