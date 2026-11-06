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
extern u32 native_fn_02008c58();
extern u32 native_fn_0202a164();
extern u32 native_fn_0204617c();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0205dbf0();
extern u32 native_fn_0205df8c();
extern u32 native_fn_02084920();
extern u32 native_fn_020c1898();
extern u32 native_fn_ov006_021d8154();
extern u8 native_data_020dc348[];
extern u8 native_data_020dc368[];
extern u8 native_data_ov006_0220c8a0[];
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
} Record_native_data_ov006_0220e9a0;
extern Record_native_data_ov006_0220e9a0 native_data_ov006_0220e9a0;
extern u8 native_data_ov006_0220e9c8[];
u32 native_ov006_021d7730(void) {
    native_fn_ov006_021d8154();
    native_fn_020485b4(native_data_ov006_0220e9a0.field_10);
    native_fn_020484dc(0, *native_data_ov006_0220c8a0);
    native_fn_0204617c(0, 2);
    native_fn_02084920();
    native_fn_0205dbf0(1, native_data_ov006_0220e9c8, native_data_020dc368, native_data_020dc348, 0x10);
    native_fn_0205df8c(0);
    native_fn_0202a164(2);
    native_fn_0202a164(1);
    native_fn_02008c58(0, 0x06000000, 0x80000);
    native_fn_02008c58(0, 0x06200000, 0x80000);
    return native_fn_020c1898(0);
}
