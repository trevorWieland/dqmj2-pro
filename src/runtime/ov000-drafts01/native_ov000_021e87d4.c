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
extern u32 native_fn_02042be8();
extern u32 native_fn_02042c0c();
extern u32 native_fn_ov000_021e035c();
extern u32 native_fn_ov000_021e858c();
extern u32 native_fn_ov000_021e8690();
extern u8 native_data_ov000_0223526c[];
u32 native_ov000_021e87d4(void) {
    s32 var_r4;
    u32 var_r5;
    u8 *var_r6;

    var_r4 = 0;
    var_r6 = native_data_ov000_0223526c;
    var_r5 = 0;
    do {
        if ((M2C_FIELD(var_r6, u8 *, 0x274) != 0) && (M2C_FIELD(var_r6, u8 *, 0x1E2) != 0)) {
            native_fn_ov000_021e858c(var_r6);
            native_fn_ov000_021e8690(var_r6);
            native_fn_02042c0c(var_r6, native_fn_ov000_021e035c(var_r6 + 0x70));
            var_r5 += 1;
            M2C_FIELD(var_r6, u8 *, 0x161) = (u8) (M2C_FIELD(var_r6, u8 *, 0x161) + 1);
        }
        native_fn_02042be8(var_r6);
        var_r4 += 1;
        var_r6 += 0x2CC;
    } while (var_r4 < 8);
    return var_r5;
}
