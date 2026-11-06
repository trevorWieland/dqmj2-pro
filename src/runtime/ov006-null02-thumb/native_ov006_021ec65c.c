#define NULL ((void *)0)
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
extern u32 native_fn_ov006_021ebb2c();
extern u8 native_data_ov006_02219b4c[];
u32 native_ov006_021ec65c(void) {
    u8 *var_r0;

    if (M2C_FIELD(native_data_ov006_02219b4c, s32 *, 0xC) != 0) {
        native_fn_ov006_021ebb2c();
        M2C_FIELD(native_data_ov006_02219b4c, s32 *, 0xC) = 0;
    }
    var_r0 = M2C_FIELD(native_data_ov006_02219b4c, u8 **, 4);
    if (var_r0 != NULL) {
        native_fn_ov006_021ebb2c();
        var_r0 = native_data_ov006_02219b4c;
        M2C_FIELD(native_data_ov006_02219b4c, u8 **, 4) = NULL;
    }
    return (u32) var_r0;
}
