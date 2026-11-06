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
extern u32 native_fn_0202a498();
extern u32 native_fn_02048308();
extern u32 native_fn_0205fd4c();
extern u32 native_fn_ov001_021fc540();
extern u32 native_fn_ov001_021fc588();
extern u32 native_fn_ov001_021fc63c();
typedef struct {
    u8 unknown_0[0xc8];
    s32 field_c8;
    s8 field_cc;
} Record_native_data_ov001_02239e7c;
extern Record_native_data_ov001_02239e7c native_data_ov001_02239e7c;
u32 native_ov001_021ff1f8(void) {
    native_fn_ov001_021fc540();
    native_fn_ov001_021fc588();
    native_fn_ov001_021fc63c();
    native_fn_02048308();
    if (native_data_ov001_02239e7c.field_c8 != 0) {
        native_fn_0202a498(native_data_ov001_02239e7c.field_cc);
    }
    return native_fn_0205fd4c(0, 0);
}
