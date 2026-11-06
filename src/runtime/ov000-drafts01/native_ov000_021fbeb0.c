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
extern u32 native_fn_0202a37c();
extern u32 native_fn_020620e8();
extern u32 native_fn_02062a50();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_ov000_021fbf44();
extern u32 native_fn_ov000_021fdddc();
extern u32 native_fn_ov000_021fdde4();
extern u32 native_fn_ov000_02215a14();
typedef struct {
    u8 unknown_0[0xc];
    u32 field_c;
} Record_native_data_ov000_022372a8;
extern Record_native_data_ov000_022372a8 native_data_ov000_022372a8;
u32 native_ov000_021fbeb0(void) {
    if (native_data_ov000_022372a8.field_c == 0) {
        native_data_ov000_022372a8.field_c = native_fn_0202a37c(2, 0x604, 4);
    }
    native_fn_02008c58(0, native_data_ov000_022372a8.field_c, 0x604);
    native_fn_ov000_02215a14();
    native_fn_ov000_021fdde4();
    M2C_FIELD(native_data_ov000_022372a8.field_c, s32 *, 0) = 0;
    M2C_FIELD(native_data_ov000_022372a8.field_c, s32 *, 4) = 6;
    native_fn_020620e8(1, 1);
    native_fn_02062a50(0);
    native_fn_0206dcd0();
    native_fn_ov000_021fdddc();
    native_fn_ov000_021fbf44();
    return 0U;
}
