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
extern u32 native_fn_0204983c();
extern u32 native_fn_02049d50();
extern u32 native_fn_0204b77c();
extern u32 native_fn_ov006_021dec9c();
extern u32 native_fn_ov006_021df140();
extern u32 native_fn_ov006_021df1dc();
extern u32 native_fn_ov006_021dff10();
extern u8 native_data_ov006_0220f654[];
extern u8 native_data_ov006_0220f69c[];
extern u8 native_data_ov006_0220f6e4[];
typedef struct {
    u8 unknown_0[0x1c];
    s8 field_1c;
} Record_native_data_ov006_0220f72c;
extern Record_native_data_ov006_0220f72c native_data_ov006_0220f72c;
u32 native_ov006_021de760(void) {
    native_fn_ov006_021df1dc();
    native_fn_ov006_021dff10();
    native_fn_ov006_021dec9c();
    native_fn_0204983c(native_data_ov006_0220f72c.field_1c, 3);
    native_fn_0204983c(native_data_ov006_0220f72c.field_1c, 0x7F);
    native_fn_0204983c(0x7F, 0);
    native_fn_0204983c(0x7F, 1);
    native_fn_0204983c(0x7F, 0xC);
    native_fn_0204983c(0x7F, 2);
    native_fn_0204983c(0x7F, 5);
    native_fn_0204983c(0x7F, 6);
    native_fn_0204983c(0x7F, 7);
    native_fn_0204983c(0x7F, 8);
    native_fn_0204b77c(native_data_ov006_0220f654);
    native_fn_0204b77c(native_data_ov006_0220f69c);
    native_fn_0204b77c(native_data_ov006_0220f6e4);
    native_fn_ov006_021df140();
    native_fn_0204b77c();
    return native_fn_02049d50();
}
