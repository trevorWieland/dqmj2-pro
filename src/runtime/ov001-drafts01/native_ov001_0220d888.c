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
extern u32 ov001_record_is_active_021db8d0();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    s8 field_2;
    u8 unknown_3[0x9];
    s32 field_c;
} Record_native_data_ov001_0223e0d8;
extern Record_native_data_ov001_0223e0d8 native_data_ov001_0223e0d8;
u32 native_ov001_0220d888(void) {
    if ((ov001_record_is_active_021db8d0(native_data_ov001_0223e0d8.field_c) != 0) && ((s32) native_data_ov001_0223e0d8.field_1 > 0)) {
        native_data_ov001_0223e0d8.field_2 = 5;
    } else {
        native_data_ov001_0223e0d8.field_2 = 2;
    }
    return 1U;
}
