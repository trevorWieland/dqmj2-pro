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
extern u32 native_fn_0205dc70();
typedef struct {
    u8 unknown_0[0x24];
    u8 field_24;
    u8 field_25;
    u16 field_26;
} Record_native_data_ov000_0224532c;
extern Record_native_data_ov000_0224532c native_data_ov000_0224532c;
u32 native_ov000_02216414(void) {
    return native_fn_0205dc70(native_data_ov000_0224532c.field_24, native_data_ov000_0224532c.field_25, native_data_ov000_0224532c.field_26);
}
