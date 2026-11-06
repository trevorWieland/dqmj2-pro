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
extern u32 native_fn_ov006_021ed9d4();
extern u32 native_fn_ov006_021edb7c();
extern u32 native_fn_ov006_021edcb8();
extern u32 native_fn_ov006_021edcd0();
extern u8 native_data_ov006_0220d448[];
u32 native_ov006_021ece60(void *arg0, void *arg1) {
    u32 var_r4;
    u32 temp_r6;

    var_r4 = 0;
    native_fn_ov006_021ed9d4(arg1, 8, native_data_ov006_0220d448, native_fn_ov006_021edcd0(native_data_ov006_0220d448));
    if (native_fn_ov006_021edb7c(arg0, arg1, 6) != 0) {
        var_r4 = -1U;
    } else {
        temp_r6 = native_fn_ov006_021edcb8(M2C_FIELD(arg0, u16 *, 6));
        if ((temp_r6 + 1) != native_fn_ov006_021edcb8(M2C_FIELD(arg1, u16 *, 6))) {
            var_r4 = -2U;
        }
    }
    return var_r4;
}
