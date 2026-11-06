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
extern u32 native_fn_02028dac();
extern u32 native_fn_020297e0();
extern u32 native_fn_02029950();
extern u32 native_fn_0204124c();
extern u8 native_data_ov000_0222f850[];
extern u8 native_data_ov000_02243e3c[];
u32 native_ov000_02212e1c(s32 arg0) {
    s32 temp_r4;
    s32 var_r0;

    var_r0 = arg0;
    if (var_r0 < 0) {
        var_r0 = (s32) (s8) *native_data_ov000_0222f850;
    }
    if (var_r0 >= 0) {
        temp_r4 = (var_r0 * 0x10C) + (s32) native_data_ov000_02243e3c;
        if (M2C_FIELD(temp_r4, u8 *, 0x105) != 0) {
            native_fn_0204124c(temp_r4);
            native_fn_02029950(temp_r4);
            native_fn_020297e0(temp_r4);
            native_fn_02028dac(temp_r4);
            M2C_FIELD(temp_r4, u8 *, 0x105) = 0U;
        }
    }
    return 0U;
}
