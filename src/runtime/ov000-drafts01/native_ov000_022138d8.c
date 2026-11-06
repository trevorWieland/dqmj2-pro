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
extern u32 native_fn_ov000_02212c08();
extern u8 native_data_ov000_02243e3c[];
u32 native_ov000_022138d8(void) {
    s32 var_r4;
    s32 var_r5;
    u8 *var_r6;

    var_r5 = 0;
    var_r6 = native_data_ov000_02243e3c;
    do {
        if (M2C_FIELD(var_r6, u8 *, 0x105) != 0) {
            native_fn_0204124c(var_r6);
            native_fn_02029950(var_r6);
            native_fn_020297e0(var_r6);
            native_fn_02028dac(var_r6);
            M2C_FIELD(var_r6, u8 *, 0x105) = 0U;
        }
        var_r5 += 1;
        var_r6 += 0x10C;
    } while (var_r5 < 0x10);
    var_r4 = 0;
    do {
        native_fn_ov000_02212c08(var_r4);
        var_r4 += 1;
    } while (var_r4 < 8);
    return 0U;
}
