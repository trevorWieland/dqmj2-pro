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
extern u32 native_fn_0202a51c();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0205f920();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x7];
    s32 field_8;
    s32 field_c;
    s32 field_10;
} Record_native_data_ov000_02236a84;
extern Record_native_data_ov000_02236a84 native_data_ov000_02236a84;
u32 native_ov000_021ebb88(void) {
    if (native_data_ov000_02236a84.field_8 != 0) {
        native_fn_020485b4();
    }
    native_fn_020484dc(1, native_data_ov000_02236a84.field_0);
    native_fn_0205f920(native_data_ov000_02236a84.field_10, 1, 2);
    native_fn_0202a51c(native_data_ov000_02236a84.field_10);
    native_fn_0205f920(native_data_ov000_02236a84.field_c, 1, 2);
    return native_fn_0202a51c(native_data_ov000_02236a84.field_c);
}
