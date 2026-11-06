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
    u8 unknown_0[0x14];
    u32 field_14;
    u8 unknown_18[0x8];
    s32 field_20;
    u8 unknown_24[0x38];
    s32 field_5c;
    u8 unknown_60[0x4];
    u32 field_64;
} Record_native_data_ov006_02218d90;
extern Record_native_data_ov006_02218d90 native_data_ov006_02218d90;
u32 native_ov006_021e8044(u32 arg0, s32 arg1) {
    u32 temp_ip;

    temp_ip = native_data_ov006_02218d90.field_64;
    native_data_ov006_02218d90.field_14 = temp_ip;
    native_data_ov006_02218d90.field_20 = (s32) native_data_ov006_02218d90.field_5c;
    native_data_ov006_02218d90.field_64 = arg0;
    native_data_ov006_02218d90.field_5c = arg1;
    return temp_ip;
}
