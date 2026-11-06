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
extern u32 native_fn_01ffb500();
extern u32 native_fn_01ffb50c();
extern u32 native_fn_020894bc();
extern u32 native_fn_ov000_021f4774();
extern u32 native_fn_ov000_021f47ec();
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
} Record_native_data_ov000_02236ee4;
extern Record_native_data_ov000_02236ee4 native_data_ov000_02236ee4;
u32 native_ov000_021f4b98(void) {
    s32 temp_r2;
    s32 var_r4;

    temp_r2 = *(s32 *) native_fn_020894bc();
    if (native_data_ov000_02236ee4.field_1 & 1) {
        var_r4 = 0;
        if (temp_r2 & 0x20000000) {
            var_r4 = 1;
        }
        if (*(u16 *) native_fn_01ffb500() == 0xFF) {
            native_fn_01ffb50c(0x1D, 0x10, 2, 5U, 0);
        } else {
            native_fn_01ffb50c(0x1D, 0x10, 0xD, (u16) (var_r4 + 0x6B), 0);
        }
        native_fn_ov000_021f47ec(1);
    } else {
        native_fn_ov000_021f47ec(2);
    }
    return native_fn_ov000_021f4774();
}
