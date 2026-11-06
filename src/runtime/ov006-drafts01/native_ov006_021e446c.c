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
extern u32 native_fn_02064510();
extern u32 native_fn_ov006_021e3cd8();
extern u32 native_fn_ov006_021e3f28();
extern u32 native_fn_ov006_021e9268();
typedef struct {
    s32 field_0;
    u32 field_4;
} Record_native_data_ov006_02218d24;
extern Record_native_data_ov006_02218d24 native_data_ov006_02218d24;
u32 native_ov006_021e446c(u32 arg0) {
    switch (native_data_ov006_02218d24.field_0) {
    case 1:
        if (native_fn_02064510() != 0) {
            native_data_ov006_02218d24.field_0 = 2;
        }
        break;
    case 2:
        if ((u32) native_data_ov006_02218d24.field_4 > 0x1EU) {
            native_fn_ov006_021e9268();
            native_fn_ov006_021e3f28(arg0);
            native_data_ov006_02218d24.field_0 = 0;
        }
        native_data_ov006_02218d24.field_4 = (u32) (native_data_ov006_02218d24.field_4 + 1);
        break;
    }
    return native_fn_ov006_021e3cd8();
}
