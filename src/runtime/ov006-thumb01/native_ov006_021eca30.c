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
extern u32 native_fn_ov006_021ecad0();
extern u32 native_fn_ov006_021ecbac();
extern u32 native_fn_ov006_021ecc84();
extern u32 native_fn_ov006_021ecd28();
extern u32 native_fn_ov006_021edcb8();
u32 native_ov006_021eca30(u32 arg0, void *arg1, s32 *arg2, s32 arg3) {
    u32 temp_r0;
    u32 var_r5;
    void *temp_r7;
    s32 sp0;

    var_r5 = arg0;
    sp0 = arg3;
    temp_r7 = arg1 + 0xC;
    if (native_fn_ov006_021edcb8(M2C_FIELD(arg1, u16 *, 0xC)) < 1U) {
        *arg2 += 1;
        return var_r5;
    }
    if (M2C_FIELD(temp_r7, u8 *, 0xF) != 0x11) {
        *arg2 += 1;
        return var_r5;
    }
    if ((s32) native_fn_ov006_021ecd28(arg1 + 0xC) > 0) {
        *arg2 += 1;
        return var_r5;
    }
    temp_r0 = native_fn_ov006_021edcb8(M2C_FIELD(temp_r7, u16 *, 6));
    switch (temp_r0) {
    case 0x1010:
        var_r5 = native_fn_ov006_021ecad0(var_r5, arg1, arg2, sp0);
        break;
    case 0x2010:
        var_r5 = native_fn_ov006_021ecbac(var_r5, arg1, arg2, sp0);
        break;
    case 0x3010:
        var_r5 = native_fn_ov006_021ecc84(var_r5, arg1, arg2, sp0);
        break;
    }
    return var_r5;
}
