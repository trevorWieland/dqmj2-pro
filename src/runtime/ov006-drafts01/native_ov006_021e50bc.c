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
extern u32 ov006_forward_four_args_021e3cd8();
extern u32 native_fn_ov006_021e3f28();
extern u32 ov006_active_state_value_021e65a4();
extern u32 native_fn_ov006_021e802c();
typedef struct {
    u8 unknown_0[0x14];
    s32 field_14;
    s32 field_18;
} Record_native_data_ov006_02218d30;
extern Record_native_data_ov006_02218d30 native_data_ov006_02218d30;
u32 native_ov006_021e50bc(void) {
    u32 temp_r0;

    temp_r0 = ov006_active_state_value_021e65a4();
    if (temp_r0 != -4U) {
        if (temp_r0 == -3U) {
            native_fn_ov006_021e3f28(0x3A);
        }
    } else {
        native_fn_ov006_021e802c(native_data_ov006_02218d30.field_18);
        native_fn_ov006_021e3f28(native_data_ov006_02218d30.field_14);
    }
    return ov006_forward_four_args_021e3cd8();
}
