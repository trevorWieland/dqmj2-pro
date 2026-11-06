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
extern u32 native_fn_020282a8();
extern u32 native_fn_0202834c();
extern u32 native_fn_0203cb2c();
extern u32 native_fn_0203cb64();
extern u32 native_fn_0203d0e4();
extern u32 native_fn_02041898();
extern u32 native_fn_020418b0();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
} Record_native_data_ov000_02247568;
extern Record_native_data_ov000_02247568 native_data_ov000_02247568;
u32 native_ov000_0222a494(void) {
    native_fn_02041898(2);
    native_fn_020418b0(2);
    native_fn_0203cb2c();
    native_fn_0203cb64();
    *(u16 *)0x04000304 |= 0x8000;
    native_fn_0203d0e4(0);
    native_fn_0202834c(0, native_data_ov000_02247568.field_4);
    return native_fn_020282a8(0, native_data_ov000_02247568.field_8);
}
