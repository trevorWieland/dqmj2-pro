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
extern u32 native_fn_02008d78();
extern u32 native_fn_02046120();
extern u32 native_fn_02046138();
typedef struct {
    s32 field_0;
    s32 field_4;
} Record_native_data_ov000_02238514;
extern Record_native_data_ov000_02238514 native_data_ov000_02238514;
extern u8 native_data_ov000_02238520[];
u32 native_ov000_02208dcc(void) {
    native_data_ov000_02238514.field_4 = 0;
    native_data_ov000_02238514.field_0 = 0;
    native_fn_02008d78(native_data_ov000_02238520, 0, 0x4C);
    M2C_FIELD(native_data_ov000_02238520, s8 *, 0xA) = 1;
    native_fn_02046120(0);
    return native_fn_02046138(0);
}
