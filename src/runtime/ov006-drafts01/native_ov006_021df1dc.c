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
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u8 native_data_ov006_0220d0bc[];
typedef struct {
    u8 unknown_0[0x24];
    s32 field_24;
    u8 unknown_28[0x34];
    s32 field_5c;
} Record_native_data_ov006_0220f594;
extern Record_native_data_ov006_0220f594 native_data_ov006_0220f594;
u32 native_ov006_021df1dc(void) {
    if (*native_data_ov006_0220d0bc == 0x7F) {
        return (u32) *native_data_ov006_0220d0bc;
    }
    native_fn_020485b4(native_data_ov006_0220f594.field_24);
    native_fn_020484dc(1, *native_data_ov006_0220d0bc);
    native_data_ov006_0220f594.field_24 = 0;
    native_data_ov006_0220f594.field_5c = 0;
    *native_data_ov006_0220d0bc = 0x7F;
    return (u32) native_data_ov006_0220d0bc;
}
