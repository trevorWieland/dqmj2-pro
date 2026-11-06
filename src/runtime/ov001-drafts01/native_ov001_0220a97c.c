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
extern u32 native_fn_02049130();
extern u32 native_fn_0204b61c();
extern u32 native_fn_0205f9e4();
extern u32 native_fn_0206b35c();
extern u32 native_fn_ov001_0220a5c0();
extern u8 native_data_02101ae8[];
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov001_0223df2c;
extern Record_native_data_ov001_0223df2c native_data_ov001_0223df2c;
u32 native_ov001_0220a97c(u32 arg0) {
    if (native_fn_ov001_0220a5c0() == 3) {
        native_fn_02049130(arg0, 0xC, native_data_ov001_0223df2c.field_c);
        native_fn_0205f9e4(native_data_ov001_0223df2c.field_c);
    } else {
        native_fn_0204b61c(native_data_ov001_0223df2c.field_c, 0);
    }
    if (native_fn_ov001_0220a5c0() == 1) {
        native_fn_0206b35c();
    }
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
