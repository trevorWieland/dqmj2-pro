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
extern u32 native_fn_02002480();
extern u32 native_fn_ov006_021fb4cc();
extern u32 native_fn_ov006_021fedc8();
extern u8 native_data_ov006_0220b7e4[];
typedef struct {
    u8 field_0;
    u8 unknown_1[0x1];
    u8 field_2;
    u8 unknown_3[0x1];
    u16 field_4;
} Record_native_data_ov006_0221c0ec;
extern Record_native_data_ov006_0221c0ec native_data_ov006_0221c0ec;
u32 native_ov006_021fb550(void) {
    s32 temp_r2;
    u32 temp_r4;

    if ((u32) (u8) (native_data_ov006_0221c0ec.field_0 + 0xF5) <= 2U) {
        return native_fn_ov006_021fb4cc();
    }
    temp_r4 = native_fn_ov006_021fedc8();
    temp_r2 = native_data_ov006_0221c0ec.field_2 + native_fn_02002480(native_data_ov006_0221c0ec.field_4, 0x1D);
    switch (temp_r2) {
    case 2:
        if (M2C_FIELD(temp_r4, u8 *, 0xF5) != 0) {
            native_data_ov006_0221c0ec.field_0 = 2;
        } else {
            native_data_ov006_0221c0ec.field_0 = 3;
        }
        break;
    case 6:
        if (M2C_FIELD(temp_r4, u8 *, 0xF6) != 0) {
            native_data_ov006_0221c0ec.field_0 = 7;
        } else {
            native_data_ov006_0221c0ec.field_0 = 8;
        }
        break;
    default:
        native_data_ov006_0221c0ec.field_0 = native_data_ov006_0220b7e4[temp_r2];
        break;
    }
    return native_fn_ov006_021fb4cc();
}
