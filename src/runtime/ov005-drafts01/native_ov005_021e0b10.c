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
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u8 native_data_ov005_021e74a8[];
typedef struct {
    u8 unknown_0[0x1c];
    s32 field_1c;
    u8 unknown_20[0xc];
    s32 field_2c;
} Record_native_data_ov005_021ed234;
extern Record_native_data_ov005_021ed234 native_data_ov005_021ed234;
u32 native_ov005_021e0b10(void) {
    if (*native_data_ov005_021e74a8 == 0x7F) {
        return (u32) *native_data_ov005_021e74a8;
    }
    native_fn_020485b4(native_data_ov005_021ed234.field_2c);
    native_fn_020484dc(1, *native_data_ov005_021e74a8);
    native_data_ov005_021ed234.field_2c = 0;
    native_data_ov005_021ed234.field_1c = 0;
    *native_data_ov005_021e74a8 = 0x7F;
    return (u32) native_data_ov005_021e74a8;
}
