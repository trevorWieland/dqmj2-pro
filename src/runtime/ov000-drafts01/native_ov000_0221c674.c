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
extern u32 native_fn_02008d78();
extern u32 native_fn_02049ad0();
extern u32 native_fn_ov000_0221c6e4();
extern u32 native_fn_ov000_0221f46c();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
    s32 field_c;
} Record_native_data_ov000_022461c4;
extern Record_native_data_ov000_022461c4 native_data_ov000_022461c4;
extern u8 native_data_ov000_022461f8[];
u32 native_ov000_0221c674(void) {
    s8 var_r6;

    native_data_ov000_022461c4.field_c = 0;
    native_data_ov000_022461c4.field_8 = 1;
    native_fn_02008d78(native_data_ov000_022461f8, 0, 0x21);
    var_r6 = 0;
    do {
        native_fn_02008c58(0, native_fn_02049ad0(var_r6), 0xC);
        var_r6 += 1;
    } while ((s32) var_r6 < 0x21);
    native_fn_ov000_0221f46c();
    return native_fn_ov000_0221c6e4();
}
