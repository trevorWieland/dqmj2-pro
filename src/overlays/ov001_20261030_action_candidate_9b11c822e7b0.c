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
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dc108();
extern u32 native_fn_ov001_021e6ec4(void *, u32, u32, s32);
extern u32 native_fn_ov001_021e6fd8(void *, u32, u32, u32);
extern u32 native_fn_ov001_021e7244();
extern u32 native_fn_ov001_0220ee24();
u32 native_ov001_021e7290(void *arg0, u32 arg1, u32 arg2, s16 *arg3, u8 *arg4, u8 *arg5) {
    s32 temp_r0;
    u32 var_r4;
    u32 temp_r5;
    u8 var_r6;
    u32 var_r8;
    u32 var_r9;

    var_r9 = arg1;
    temp_r5 = native_fn_ov001_0220ee24(0U);
    if ((native_fn_ov001_021db8d0(arg0) != 0) && (native_fn_ov001_021dc108(arg0) != 0)) {
        if (M2C_FIELD(arg0, s8 *, 0x237) != 0) {
            if ((s32) native_fn_0207b674(0x40, M2C_FIELD(arg0, void **, 0x1E8) + 0x46) <= 0) {
                temp_r0 = (s32) native_fn_0203d294(8);
                if (temp_r0 < 5) {
                    var_r4 = 0xCB;
                } else if (temp_r0 < 7) {
                    var_r4 = 0xCC;
                } else {
                    var_r4 = 0xCD;
                }
            } else {
                var_r4 = 0xD9;
            }
        } else if ((u32) M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xAA) <= 3U) {
            var_r4 = native_fn_ov001_021e6ec4(arg0, var_r9, arg2, M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xAA));
        } else {
            var_r4 = native_fn_ov001_021e6fd8(arg0, var_r9, arg2, M2C_FIELD(M2C_FIELD(arg0, void **, 0x1E8), u8 *, 0xAA));
        }
        if ((((u32) (M2C_FIELD((void *) native_fn_0207afec(var_r4), u16 *, 8) << 0x18) >> 0x1C) == 0) || (((u32) (M2C_FIELD((void *) native_fn_0207afec(var_r4), u16 *, 8) << 0x18) >> 0x1C) == 2)) {
            var_r6 = M2C_FIELD(arg0, u8 *, 0x31E);
        } else if (M2C_FIELD(arg0, u8 *, 0x31E) == 0) {
            var_r6 = 1;
        } else {
            var_r6 = 0;
        }
        if (((u32) (M2C_FIELD((void *) native_fn_0207afec(var_r4), u16 *, 8) << 0x18) >> 0x1C) != 2) {
            if (var_r6 != M2C_FIELD(arg0, u8 *, 0x31E)) {
                var_r9 = arg2;
            }
            var_r8 = native_fn_ov001_021e7244(arg0, var_r9, var_r4);
        } else {
            var_r8 = (u32) M2C_FIELD(arg0, u8 *, 0x31F);
        }
    } else {
        var_r6 = 0;
        var_r8 = 0;
        var_r4 = 6;
    }
    native_fn_ov001_0220ee24(temp_r5);
    *arg3 = (s16) var_r4;
    *arg4 = var_r6;
    *arg5 = (u8) var_r8;
    return 1U;
}
