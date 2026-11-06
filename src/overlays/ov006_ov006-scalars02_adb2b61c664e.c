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
typedef struct {
    u8 unknown_0[0x68];
    s32 field_68;
    s32 field_6c;
} Record_native_data_ov006_0221aad0;
extern Record_native_data_ov006_0221aad0 native_data_ov006_0221aad0;
extern u8 native_data_ov006_0221ab54[];
u32 native_ov006_021ef0d8(u32 arg0) {
    u32 var_r0;
    s32 temp_r4;

    var_r0 = arg0;
    temp_r4 = native_data_ov006_0221aad0.field_68 + 1;
    if ((temp_r4 != native_data_ov006_0221aad0.field_6c) && (native_data_ov006_0221aad0.field_68 != (native_data_ov006_0221aad0.field_6c + 3))) {
        *(u32 *)(native_data_ov006_0221ab54 + (native_data_ov006_0221aad0.field_68 * 4)) = var_r0;
        native_data_ov006_0221aad0.field_68 = temp_r4;
        if (temp_r4 >= 4) {
            var_r0 = 0;
            native_data_ov006_0221aad0.field_68 = 0;
        }
    }
    return var_r0;
}
