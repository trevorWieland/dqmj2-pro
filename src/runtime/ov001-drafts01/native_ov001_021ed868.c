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
extern u32 native_fn_0207b004();
extern u32 native_fn_ov001_021dc9d4();
typedef struct {
    u8 unknown_0[0x13];
    s8 field_13;
    u8 unknown_14[0x22];
    u16 field_36;
    u8 unknown_38[0x28];
    s32 field_60;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021ed868(void) {
    if ((native_fn_0207b004(native_data_ov001_02238d7c.field_36, 0x10000000) != 0) && (native_fn_ov001_021dc9d4(native_data_ov001_02238d7c.field_60) != 0)) {
        native_data_ov001_02238d7c.field_13 = 0xD;
    } else {
        native_data_ov001_02238d7c.field_13 = 9;
    }
    return 1U;
}
