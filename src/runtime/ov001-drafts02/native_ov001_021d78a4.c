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
    u8 unknown_0[0x760];
    s8 field_760;
    s8 field_761;
    s8 field_762;
    u8 unknown_763[0x5];
    s32 field_768;
} Record_native_data_ov001_02230d50;
extern Record_native_data_ov001_02230d50 native_data_ov001_02230d50;
typedef struct {
    u8 unknown_0[0x64];
    s16 field_64;
    s16 field_66;
} Record_native_data_ov001_02231450;
extern Record_native_data_ov001_02231450 native_data_ov001_02231450;
void native_ov001_021d78a4(s8 arg0, s16 arg1, s8 arg2, s32 arg3) {
    native_data_ov001_02230d50.field_760 = 1;
    native_data_ov001_02230d50.field_761 = arg0;
    native_data_ov001_02231450.field_64 = 0;
    native_data_ov001_02231450.field_66 = arg1;
    native_data_ov001_02230d50.field_762 = arg2;
    native_data_ov001_02230d50.field_768 = arg3;
}
