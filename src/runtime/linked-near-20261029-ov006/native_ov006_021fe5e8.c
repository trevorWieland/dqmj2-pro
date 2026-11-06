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
extern u32 native_fn_02008bf8();
extern u32 native_fn_ov006_02204974();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov006_0221c134;
extern Record_native_data_ov006_0221c134 native_data_ov006_0221c134;
u32 native_ov006_021fe5e8(u32 arg0) {
    native_fn_02008bf8(native_data_ov006_0221c134.field_4, 0x05000000, 0x200);
    return native_fn_ov006_02204974(1, arg0);
}
