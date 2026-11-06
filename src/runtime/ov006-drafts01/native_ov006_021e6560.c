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
extern u32 native_fn_ov006_021e7a00();
typedef struct {
    u8 unknown_0[0x24];
    s32 field_24;
    u8 unknown_28[0x8];
    s32 field_30;
    u8 unknown_34[0xc];
    s32 field_40;
} Record_native_data_ov006_02218d90;
extern Record_native_data_ov006_02218d90 native_data_ov006_02218d90;
u32 native_ov006_021e6560(s32 arg0, s32 arg1) {
    native_data_ov006_02218d90.field_24 = arg0;
    native_data_ov006_02218d90.field_40 = 3;
    native_data_ov006_02218d90.field_30 = 2;
    if (arg1 == 0) {
        return 2U;
    }
    return native_fn_ov006_021e7a00(0);
}
