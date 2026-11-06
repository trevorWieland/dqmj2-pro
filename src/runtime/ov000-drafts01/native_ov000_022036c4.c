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
extern u32 native_fn_ov000_02202938();
extern u32 native_fn_ov000_02214a38();
typedef struct {
    u8 unknown_0[0x5];
    s8 field_5;
    u8 unknown_6[0x6];
    s16 field_c;
    s8 field_e;
} Record_native_data_ov000_02238190;
extern Record_native_data_ov000_02238190 native_data_ov000_02238190;
u32 native_ov000_022036c4(s16 arg0, s8 arg1) {
    native_data_ov000_02238190.field_c = arg0;
    native_data_ov000_02238190.field_e = arg1;
    native_fn_ov000_02202938();
    native_data_ov000_02238190.field_5 = 0;
    return native_fn_ov000_02214a38(0, 0);
}
