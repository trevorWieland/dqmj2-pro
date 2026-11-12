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
extern u32 native_fn_0204b77c();
extern u32 native_fn_ov000_02215078();
extern u32 ov000_display_context_02215698();
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov000_022372a8;
extern Record_native_data_ov000_022372a8 native_data_ov000_022372a8;
u32 native_ov000_021fde90(void) {
    native_fn_0204b77c(ov000_display_context_02215698() + 0x10);
    native_fn_ov000_02215078(native_data_ov000_022372a8.field_c + 0xB4, 1);
    return native_fn_ov000_02215078(native_data_ov000_022372a8.field_c + 0x1A4, 1);
}
