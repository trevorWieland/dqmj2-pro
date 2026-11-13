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
extern u32 native_fn_02068a0c();
extern u32 ov006_forward_four_args_021e3cd8();
extern u32 native_fn_ov006_021e3f28();
extern u32 ov006_active_state_value_021e65a4();
extern u32 native_fn_ov006_021e7e28();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov006_0220d108;
extern Record_native_data_ov006_0220d108 native_data_ov006_0220d108;
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov006_02218d70;
extern Record_native_data_ov006_02218d70 native_data_ov006_02218d70;
u32 native_ov006_021e5f1c(void) {
    if (ov006_active_state_value_021e65a4() != 0) {
        native_fn_02068a0c(native_data_ov006_0220d108.field_8);
        native_data_ov006_02218d70.field_8 = 1;
        native_fn_ov006_021e7e28();
        native_fn_ov006_021e3f28(0x58);
    }
    return ov006_forward_four_args_021e3cd8();
}
