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
extern u32 native_fn_ov001_021e1328();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x7];
    u32 field_8;
} Record_native_data_ov001_02242c40;
extern Record_native_data_ov001_02242c40 native_data_ov001_02242c40;
u32 native_ov001_02217a94(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov001_021e1328();
    native_data_ov001_02242c40.field_8 = temp_r0;
    native_data_ov001_02242c40.field_0 = 0;
    return temp_r0;
}
