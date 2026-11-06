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
extern u32 native_fn_0201d444();
extern u32 native_fn_02040838();
extern u32 native_fn_02040884();
extern u32 native_fn_02040dc0();
extern u32 native_fn_ov000_021dfafc();
extern u8 native_data_ov000_0222bad0[];
extern u8 native_data_ov000_0222f814[];
extern u8 native_data_ov000_02240fbc[];
u32 native_ov000_02211210(u32 arg0) {
    u8 sp0[32];
    u32 temp_r0;
    u32 var_r5;

    var_r5 = 0;
    if ((arg0 < 0x136U) && (native_fn_02040838(arg0, native_data_ov000_02240fbc, 0x10) == 0)) {
        temp_r0 = native_fn_02040884(arg0, native_data_ov000_02240fbc, 0x10);
        if (temp_r0 != 0) {
            native_fn_0201d444(&sp0, native_data_ov000_0222f814, native_fn_ov000_021dfafc(arg0, 0));
            var_r5 = native_fn_02040dc0(temp_r0, native_data_ov000_0222bad0, &sp0, 1);
        }
    }
    return var_r5;
}
