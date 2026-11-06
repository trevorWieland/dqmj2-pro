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
extern u32 native_fn_020c1e50();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x7];
    s32 field_8;
} Record_native_data_ov000_022476f0;
extern Record_native_data_ov000_022476f0 native_data_ov000_022476f0;
extern u8 native_data_ov000_022476fc[];
extern u8 native_data_ov000_02247700[];
u32 native_ov000_0222afb8(void) {
    if (native_data_ov000_022476f0.field_8 != 0) {
        native_fn_020485b4();
    }
    native_fn_020484dc(1, native_data_ov000_022476f0.field_0);
    native_fn_020c1e50(2, native_data_ov000_02247700);
    return native_fn_020c1e50(2, native_data_ov000_022476fc);
}
