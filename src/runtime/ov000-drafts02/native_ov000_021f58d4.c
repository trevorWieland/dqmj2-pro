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
    u8 unknown_0[0x4];
    s32 field_4;
    u8 unknown_8[0xc];
    u32 field_14;
    s32 field_18;
    u8 unknown_1c[0x8];
    s32 field_24;
} Record_native_data_ov000_02236ee4;
extern Record_native_data_ov000_02236ee4 native_data_ov000_02236ee4;
void native_ov000_021f58d4(s32 arg0, s32 arg1, s32 arg2) {
    u32 temp_ip;

    temp_ip = arg2 + (arg0 + arg1);
    native_data_ov000_02236ee4.field_14 = temp_ip;
    native_data_ov000_02236ee4.field_24 = arg0;
    native_data_ov000_02236ee4.field_18 = arg1;
    native_data_ov000_02236ee4.field_4 = arg2;
    if (temp_ip > 0x3E7U) {
        native_data_ov000_02236ee4.field_14 = 0x3E7U;
    }
}
