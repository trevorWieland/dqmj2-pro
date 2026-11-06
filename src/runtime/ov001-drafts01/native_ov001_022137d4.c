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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048e8c();
extern u32 native_fn_0206c644();
extern u32 native_fn_0206c6c0();
extern u32 native_fn_0206c87c();
extern u32 native_fn_ov001_0221395c();
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 unknown_2[0x2];
    s32 field_4;
    s32 field_8;
} Record_native_data_ov001_02242998;
extern Record_native_data_ov001_02242998 native_data_ov001_02242998;
extern u8 native_data_ov001_0224299c[];
u32 native_ov001_022137d4(void) {
    native_data_ov001_02242998.field_1 = (s8) native_fn_0202a1e0(2);
    native_fn_02048e74(native_data_ov001_0224299c, 2);
    native_data_ov001_02242998.field_8 = 0;
    native_data_ov001_02242998.field_4 = 0;
    native_fn_ov001_0221395c();
    native_fn_02048e8c();
    native_fn_0202a1e0(native_data_ov001_02242998.field_1);
    native_data_ov001_02242998.field_0 = (u8) native_data_ov001_02242998.field_4;
    native_fn_0206c644();
    native_fn_0206c87c(0);
    return native_fn_0206c6c0(2);
}
