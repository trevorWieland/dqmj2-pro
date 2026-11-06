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
extern u32 native_fn_020072d0();
extern u32 native_fn_020072ec();
extern u32 native_fn_020118a4();
extern u32 native_fn_020119c0();
extern u32 native_fn_02011a34();
u32 native_main_020130e8(s32 arg0, s32 arg1, s32 arg2, u32 arg3, u16 arg4, u16 arg5, u16 arg6) {
    u16 var_r4;
    u32 temp_r0;
    u32 var_r0;
    void *temp_r5;

    var_r4 = 1;
    temp_r5 = M2C_FIELD((void *) native_fn_020119c0(), void **, 4);
    temp_r0 = native_fn_02011a34(2, 9, 0xA);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    native_fn_020072d0(temp_r5 + 0x188, 2);
    if (M2C_FIELD(temp_r5, u16 *, 0x188) == 0) {
        native_fn_020072d0(temp_r5 + 0x182, 2);
        var_r4 = M2C_FIELD(temp_r5, u16 *, 0x182);
        native_fn_020072d0(temp_r5 + 0x86, 2);
    }
    if (arg2 == 0) {
        return 6U;
    }
    if (var_r4 == 0) {
        return 7U;
    }
    native_fn_020072d0(temp_r5 + 0x7C, 2);
    if (arg2 == M2C_FIELD(temp_r5, s32 *, 0x7C)) {
        return 6U;
    }
    if (arg3 > 0x200U) {
        return 6U;
    }
    if (arg3 == 0) {
        return 6U;
    }
    native_fn_020072ec(arg2, arg3);
    var_r0 = native_fn_020118a4(0xF, 7, arg2, arg3, (s32) arg4, (s32) arg5, (s32) arg6, arg0, arg1);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
