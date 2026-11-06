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
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fdc78();
extern u32 native_fn_ov006_02200584();
extern u32 native_fn_ov006_022031a0();
u32 native_ov006_021fdc54(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02200584();
    if (var_r0 == 0) {
        native_fn_ov006_022031a0(3, 0, 0x14, 8);
        var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021fdc78);
    }
    return var_r0;
}
