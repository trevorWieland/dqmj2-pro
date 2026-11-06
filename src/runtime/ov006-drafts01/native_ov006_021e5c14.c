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
extern u32 native_fn_ov006_021e3cd4();
extern u32 native_fn_ov006_021e57d0();
extern u32 native_fn_ov006_021e6560();
extern u32 native_fn_ov006_021e802c();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov006_0220d108;
extern Record_native_data_ov006_0220d108 native_data_ov006_0220d108;
u32 native_ov006_021e5c14(void) {
    u32 temp_r4;
    s32 var_r5;

    temp_r4 = native_fn_ov006_021e57d0();
    var_r5 = native_data_ov006_0220d108.field_4;
    native_fn_ov006_021e3cd4();
    if (temp_r4 == 0) {
        native_fn_ov006_021e802c(-1);
    } else if (var_r5 >= 0) {
        if (var_r5 >= (s32) temp_r4) {
            var_r5 = temp_r4 - 1;
        }
        native_fn_ov006_021e802c(var_r5);
    } else {
        native_fn_ov006_021e802c(0);
    }
    native_data_ov006_0220d108.field_4 = -1;
    return native_fn_ov006_021e6560(0x10, 0);
}
