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
    u8 unknown_0[0x5c];
    u16 field_5c;
} Record_native_data_ov001_022315bc;
extern Record_native_data_ov001_022315bc native_data_ov001_022315bc;
u32 native_ov001_021d8cc8(u16 arg0) {
    u16 temp_r2;

    temp_r2 = native_data_ov001_022315bc.field_5c;
    native_data_ov001_022315bc.field_5c = arg0;
    return (u32) temp_r2;
}
