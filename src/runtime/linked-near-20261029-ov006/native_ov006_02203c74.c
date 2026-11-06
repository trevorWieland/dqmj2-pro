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
extern u32 native_fn_02008430();
extern u32 native_fn_0200dc38();
extern u32 native_fn_0200dccc();
extern u32 native_fn_0200ded8();
extern u32 native_fn_0200e390();
extern u32 native_fn_0200e3a8();
extern u32 native_fn_ov006_02203c08();
extern u32 native_fn_ov006_02203cf0();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_ov006_0221c18c;
extern Record_native_data_ov006_0221c18c native_data_ov006_0221c18c;
u32 native_ov006_02203c74(void) {
    u8 sp0[8];

    native_data_ov006_0221c18c.field_4 = native_fn_ov006_02203c08(0x3A, 4);
    if (native_fn_0200dc38(&sp0) == 0) {
        native_fn_02008430();
    }
    native_fn_0200dccc(&sp0);
    native_fn_0200ded8(0, 4, native_data_ov006_0221c18c.field_4, 5);
    native_fn_0200e390(2);
    if (native_fn_0200e3a8(2) != 0) {
        native_fn_02008430();
    }
    return native_fn_ov006_02203cf0();
}
