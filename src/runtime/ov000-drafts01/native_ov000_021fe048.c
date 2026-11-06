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
extern u32 native_fn_020620b4();
extern u32 native_fn_ov000_021fdfac();
extern u32 native_fn_ov000_021fe1e8();
extern u32 native_fn_ov000_021fe600();
extern u32 native_fn_ov000_02215a14();
extern u32 native_fn_ov000_022162e4();
extern u32 native_fn_ov000_022179fc();
extern u32 native_fn_ov000_02217ac8();
typedef struct {
    s32 field_0;
    s32 field_4;
} Record_native_data_ov000_022372bc;
extern Record_native_data_ov000_022372bc native_data_ov000_022372bc;
extern u8 native_data_ov000_022372c4[];
u32 native_ov000_021fe048(void) {
    native_fn_ov000_021fdfac();
    native_data_ov000_022372bc.field_0 = 0;
    native_fn_020620b4(0x19);
    native_data_ov000_022372bc.field_4 = 3;
    native_fn_02008c58(0, native_data_ov000_022372c4, 0xF0);
    native_fn_ov000_022162e4();
    native_fn_ov000_02215a14();
    native_fn_ov000_021fe600();
    native_fn_ov000_022179fc();
    native_fn_ov000_02217ac8(0);
    native_fn_ov000_021fe1e8();
    return 0U;
}
