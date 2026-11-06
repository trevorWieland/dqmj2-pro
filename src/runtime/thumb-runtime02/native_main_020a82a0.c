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
extern u32 native_fn_020a5820();
extern u32 native_fn_020a7090();
extern u32 native_fn_020a7b30();
extern u32 native_fn_020a8198();
extern u32 native_fn_020a8bf0();
extern u32 native_fn_020a8d88();
u32 native_main_020a82a0(void *arg0) {
    s32 temp_r4;
    u32 temp_r0;
    u32 var_r6;

    if (native_fn_020a8d88(M2C_FIELD(arg0, s32 *, 0x6B4)) == 0) {
        return 0U;
    }
    temp_r4 = M2C_FIELD(arg0, s32 *, 0x80);
    temp_r0 = native_fn_020a8bf0(M2C_FIELD(arg0, s32 *, 0x6B4), M2C_FIELD(arg0, s32 *, 0x7C) + temp_r4, 0x1000 - temp_r4, 0);
    if ((u32) (temp_r0 + 1) <= 1U) {
        native_fn_020a7090(arg0);
        return 3U;
    }
    var_r6 = 0;
    M2C_FIELD(arg0, s32 *, 0x80) = (s32) (M2C_FIELD(arg0, s32 *, 0x80) + temp_r0);
    if ((M2C_FIELD(arg0, s32 *, 0) == 2) || ((s32) M2C_FIELD(arg0, s32 *, 0x7CC) > 0)) {
        native_fn_020a5820(arg0 + 0x6C0, M2C_FIELD(arg0, s32 *, 0x7C) + temp_r4, M2C_FIELD(arg0, s32 *, 0x80) - temp_r4);
    }
    if (M2C_FIELD(arg0, s32 *, 0) == 3) {
        var_r6 = native_fn_020a7b30(arg0);
    }
    if (var_r6 != 0) {
        return var_r6;
    }
    if ((M2C_FIELD(arg0, s32 *, 0) == 2) && ((s32) M2C_FIELD(arg0, s32 *, 0x80) > 0)) {
        return native_fn_020a8198(arg0);
    }
    return 0U;
}
