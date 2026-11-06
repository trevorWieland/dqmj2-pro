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
extern u32 native_fn_0203ca5c();
extern u32 native_fn_0203caa4();
extern u32 native_fn_02040820();
extern u32 native_fn_ov000_021dff00();
extern u8 native_data_ov000_02244efc[];
extern u8 native_data_ov000_02244f84[];
extern u8 native_data_ov000_02245028[];
extern u8 native_data_ov000_02245128[];
typedef struct {
    u8 unknown_0[0xe2];
    s16 field_e2;
} Record_native_data_ov000_02245228;
extern Record_native_data_ov000_02245228 native_data_ov000_02245228;
u32 native_ov000_02214654(void) {
    native_fn_ov000_021dff00();
    if (M2C_FIELD(M2C_FIELD(native_data_ov000_02244efc, void **, 8), s32 *, 0x30) != 0) {
        native_fn_0203ca5c(native_data_ov000_02244f84, 0);
    }
    if ((s32) native_data_ov000_02245228.field_e2 > 0) {
        native_fn_0203caa4(native_data_ov000_02245028, 0x41);
        native_fn_0203caa4(native_data_ov000_02245128, 0x41);
    }
    return native_fn_02040820();
}
