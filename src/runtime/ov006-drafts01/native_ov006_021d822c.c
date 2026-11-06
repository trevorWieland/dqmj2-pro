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
extern u32 native_fn_02048644();
extern u32 native_fn_020ba574();
typedef struct {
    u8 unknown_0[0x1c];
    s32 field_1c;
} Record_native_data_ov006_0220e9a0;
extern Record_native_data_ov006_0220e9a0 native_data_ov006_0220e9a0;
extern u8 native_data_ov006_0220ea74[];
u32 native_ov006_021d822c(void) {
    if ((s32) native_fn_020ba574() >= 0) {
        M2C_FIELD(native_data_ov006_0220ea74, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov006_0220ea74, s32 *, 0x7C) | 2);
        return native_fn_02048644(native_data_ov006_0220ea74, native_data_ov006_0220e9a0.field_1c, (u8) native_fn_020ba574());
    }
    M2C_FIELD(native_data_ov006_0220ea74, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov006_0220ea74, s32 *, 0x7C) & ~2);
    return (u32) native_data_ov006_0220ea74;
}
