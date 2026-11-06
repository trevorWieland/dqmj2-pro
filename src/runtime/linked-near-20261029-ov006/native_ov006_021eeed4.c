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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02008c28();
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_02089ef8();
extern u32 native_fn_ov006_021eecb0();
typedef struct {
    u8 unknown_0[0x28];
    s32 field_28;
    s32 field_2c;
    u8 unknown_30[0x1c];
    s32 field_4c;
    u8 unknown_50[0x8];
    s32 field_58;
} Record_native_data_ov006_0221aad0;
extern Record_native_data_ov006_0221aad0 native_data_ov006_0221aad0;
u32 native_ov006_021eeed4(u32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    native_data_ov006_0221aad0.field_58 = arg2;
    if (arg1 != 0) {
        native_fn_02008e0c(arg1, native_data_ov006_0221aad0.field_28, 0x60);
    } else {
        native_fn_02008d78(native_data_ov006_0221aad0.field_28, 0, 0x60);
    }
    native_fn_02008c28(arg0, native_data_ov006_0221aad0.field_4c, 0xC0);
    if (native_fn_ov006_021eecb0() == 1) {
        native_data_ov006_0221aad0.field_2c = 8;
        native_fn_02008008(temp_r4);
        return 1U;
    }
    if ((native_data_ov006_0221aad0.field_2c == 3) && (native_fn_02089ef8(native_data_ov006_0221aad0.field_4c, native_data_ov006_0221aad0.field_28, native_data_ov006_0221aad0.field_58) == 3)) {
        native_data_ov006_0221aad0.field_2c = 8;
        native_fn_02008008(temp_r4);
        return 1U;
    }
    native_fn_02008008(temp_r4);
    return 0U;
}
