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
extern u32 native_fn_02012764();
extern u32 native_fn_ov006_02201270();
extern u32 native_fn_ov006_022012c0();
extern u32 native_fn_ov006_02201b40();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov006_0221c164;
extern Record_native_data_ov006_0221c164 native_data_ov006_0221c164;
u32 native_ov006_02201b0c(void) {
    native_fn_ov006_02201270(3);
    if (native_fn_02012764(native_data_ov006_0221c164.field_4 + 0x80, native_fn_ov006_02201b40, 2) != 2) {
        native_fn_ov006_022012c0();
        native_fn_ov006_02201270(0xA);
        return 0U;
    }
    return 1U;
}
