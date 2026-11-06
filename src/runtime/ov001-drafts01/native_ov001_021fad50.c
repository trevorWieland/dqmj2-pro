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
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x3];
    s8 field_e;
    u8 unknown_f[0x17];
    s16 field_26;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fad50(void) {
    native_data_ov001_02239a14.field_e = (s8) (native_data_ov001_02239a14.field_e + 1);
    if ((s32) native_data_ov001_02239a14.field_e >= 3) {
        native_data_ov001_02239a14.field_a = 0xB;
    } else if ((s32) native_data_ov001_02239a14.field_26 >= 0x3E8) {
        native_data_ov001_02239a14.field_a = 0xB;
    } else {
        native_data_ov001_02239a14.field_a = 5;
    }
    return 1U;
}
