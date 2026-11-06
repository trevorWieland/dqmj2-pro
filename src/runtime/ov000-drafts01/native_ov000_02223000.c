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
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_0205e73c();
extern u32 native_fn_0205f5dc();
typedef struct {
    u8 field_0;
    u8 unknown_1[0xb];
    u32 field_c;
} Record_native_data_ov000_02246574;
extern Record_native_data_ov000_02246574 native_data_ov000_02246574;
u32 native_ov000_02223000(void) {
    native_fn_020414b0(0x3F);
    native_fn_02041510(1, 2, 0xA);
    native_data_ov000_02246574.field_0 = 8;
    native_data_ov000_02246574.field_c = native_fn_0205f5dc();
    native_fn_0205e73c(0x214);
    return native_fn_0205e73c(0x93);
}
