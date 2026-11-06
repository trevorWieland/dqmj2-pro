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
extern u32 native_fn_0206be08();
extern u32 native_fn_ov001_0220267c();
extern u32 native_fn_ov001_02203554();
extern u32 native_fn_ov001_0220364c();
extern u32 native_fn_ov001_0220375c();
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov001_0223d8fc;
extern Record_native_data_ov001_0223d8fc native_data_ov001_0223d8fc;
u32 native_ov001_02203c3c(void) {
    native_fn_ov001_02203554();
    native_fn_ov001_0220267c();
    native_fn_ov001_0220364c();
    native_fn_ov001_0220375c();
    native_fn_0206be08(0, native_data_ov001_0223d8fc.field_0);
    return native_fn_0206be08(1, native_data_ov001_0223d8fc.field_1);
}
