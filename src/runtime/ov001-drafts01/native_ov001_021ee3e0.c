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
extern u32 native_fn_ov001_021e9610();
extern u32 native_fn_ov001_021f1324();
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov001_0222ec84;
extern Record_native_data_ov001_0222ec84 native_data_ov001_0222ec84;
u32 native_ov001_021ee3e0(void) {
    native_fn_ov001_021e9610(native_data_ov001_0222ec84.field_1);
    if (native_data_ov001_0222ec84.field_0 != 0) {
        native_fn_ov001_021f1324();
    }
    return 0U;
}
