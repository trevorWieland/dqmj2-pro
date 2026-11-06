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
extern u32 native_fn_02041538();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
    s32 field_c;
} Record_native_data_ov006_0220f4e8;
extern Record_native_data_ov006_0220f4e8 native_data_ov006_0220f4e8;
u32 native_ov006_021ddf6c(void) {
    if (native_data_ov006_0220f4e8.field_8 == 2) {
        native_data_ov006_0220f4e8.field_8 = 1;
        native_data_ov006_0220f4e8.field_c = 1;
        return 1U;
    }
    native_data_ov006_0220f4e8.field_c = 0;
    return native_fn_02041538(1, 2, 0xA);
}
